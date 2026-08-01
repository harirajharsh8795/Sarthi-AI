import os
import re
import time
import sqlite3
import logging
import urllib.parse
import requests

# Safe DTensor monkeypatch for PyTorch / Transformers compatibility
try:
    import torch
    import torch.distributed
    try:
        import torch.distributed.tensor
        if not hasattr(torch.distributed.tensor, "DTensor"):
            class DTensor: pass
            torch.distributed.tensor.DTensor = DTensor
    except Exception:
        pass
except Exception:
    pass

from tqdm import tqdm
import fitz  # PyMuPDF
import langdetect
from langdetect.lang_detect_exception import LangDetectException
import uuid
import docx
import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import session_manager

# Tesseract executable configuration (Cross-platform with Windows fallback)
import shutil
system_tess = shutil.which("tesseract")
if system_tess:
    pytesseract.pytesseract.tesseract_cmd = system_tess
else:
    user_profile = os.environ.get("USERPROFILE", "")
    TESSERACT_PATHS = [
        os.path.join(user_profile, r"AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    ]
    for path in TESSERACT_PATHS:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break

# Paths
DATA_DIR = "./data"
SQLITE_DIR = os.path.join(DATA_DIR, "sqlite")
DB_PATH = os.path.join(SQLITE_DIR, "saarthi.db")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")
KB_DIR = os.path.join(DATA_DIR, "knowledge_base")

# Model configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
OCR_LOW_CONFIDENCE_THRESHOLD = 50.0

# Global lazy-loaded instances
_embedding_model = None
_chroma_client = None

def init_directories():
    """Initializes the required folder structure."""
    domains = ["constitution_and_general_law", "legal", "banking", "hospital"]
    languages = ["en", "hi"]
    
    # Create subfolders for each domain and language
    for d in domains:
        for l in languages:
            os.makedirs(os.path.join(KB_DIR, d, l), exist_ok=True)
            
    os.makedirs(SQLITE_DIR, exist_ok=True)
    os.makedirs(CHROMA_DIR, exist_ok=True)
    os.makedirs("./glossary", exist_ok=True)
    logger.debug("Folder structure initialized successfully.")

import db_manager

def get_db_connection():
    """Returns a connection to the SQLite database using the Singleton pool."""
    return db_manager.db_pool.get_connection()

def init_db():
    """Initializes the SQLite database table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kb_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            language TEXT NOT NULL,
            filename TEXT NOT NULL UNIQUE,
            source_url TEXT NOT NULL UNIQUE,
            discovered_via TEXT NOT NULL,
            page_count INTEGER,
            chunk_count INTEGER,
            status TEXT NOT NULL,
            downloaded_at TEXT,
            indexed_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.debug("SQLite database and kb_documents table initialized.")

def get_document_by_url(url):
    """Retrieves a document record from SQLite by source_url."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kb_documents WHERE source_url = ?", (url,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_all_documents():
    """Retrieves all document records from SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kb_documents")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def upsert_document_record(domain, language, filename, source_url, discovered_via, status, 
                           page_count=None, chunk_count=None, downloaded_at=None, indexed_at=None):
    """Inserts or updates a document record in SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if record exists by source_url or by filename
    cursor.execute("SELECT id FROM kb_documents WHERE source_url = ? OR filename = ?", (source_url, filename))
    row = cursor.fetchone()
    
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    
    if row:
        # Update existing record
        doc_id = row['id']
        update_fields = []
        params = []
        
        # Build dynamic update statement based on provided fields
        fields_to_update = {
            "domain": domain,
            "language": language,
            "filename": filename,
            "source_url": source_url,
            "discovered_via": discovered_via,
            "status": status
        }
        if page_count is not None:
            fields_to_update["page_count"] = page_count
        if chunk_count is not None:
            fields_to_update["chunk_count"] = chunk_count
        if downloaded_at is not None:
            fields_to_update["downloaded_at"] = downloaded_at
        if indexed_at is not None:
            fields_to_update["indexed_at"] = indexed_at
            
        for k, v in fields_to_update.items():
            update_fields.append(f"{k} = ?")
            params.append(v)
            
        params.append(doc_id)
        query = f"UPDATE kb_documents SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, tuple(params))
    else:
        # Insert new record
        cursor.execute("""
            INSERT INTO kb_documents 
            (domain, language, filename, source_url, discovered_via, page_count, chunk_count, status, downloaded_at, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (domain, language, filename, source_url, discovered_via, page_count, chunk_count, status, downloaded_at, indexed_at))
        
    conn.commit()
    conn.close()

import services

def get_embedding_model():
    """Returns the singleton sentence-transformers model from services."""
    return services.embedding_service.get_model()

def get_chroma_collection():
    """Returns the singleton ChromaDB knowledge_base collection from services."""
    return services.chroma_manager.get_collection("knowledge_base")

def download_file(url, save_path, unstable=False):
    """
    Downloads a file with streamed requests, 30s timeout, and 3 retries with exponential backoff.
    If unstable=True, verifies that the Content-Type is application/pdf before writing to disk.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    max_retries = 3
    backoff_factor = 2
    
    for attempt in range(1, max_retries + 1):
        try:
            logger.debug(f"Downloading {url} (Attempt {attempt}/{max_retries})...")
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            
            # Check response code
            if response.status_code != 200:
                logger.debug(f"Failed with HTTP Status {response.status_code}")
                time.sleep(backoff_factor ** attempt)
                continue
                
            # Content type check
            content_type = response.headers.get("Content-Type", "").lower()
            if "application/pdf" not in content_type:
                # If content-type is missing or unexpected, but it's marked unstable or looks HTML-ish
                if unstable or "text/html" in content_type:
                    logger.debug(f"Warning: URL did not resolve to a PDF. Content-Type is '{content_type}'. Skipping.")
                    return False
            
            # Save the file
            temp_path = save_path + ".tmp"
            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        
            # Rename temp to target
            if os.path.exists(save_path):
                os.remove(save_path)
            os.rename(temp_path, save_path)
            logger.debug(f"Successfully downloaded and saved to {save_path}")
            return True
            
        except Exception as e:
            logger.debug(f"Error on attempt {attempt}: {e}")
            if attempt < max_retries:
                time.sleep(backoff_factor ** attempt)
            else:
                logger.debug("Max retries exceeded.")
                
    return False

def extract_text_and_language(pdf_path, expected_lang):
    """
    Extracts text page-by-page from a PDF using PyMuPDF (fitz).
    Verifies the document language on page 1 (or first readable page) using langdetect.
    Logs warning on mismatch.
    Returns (pages_text, detected_lang).
    """
    doc = fitz.open(pdf_path)
    pages_text = []
    
    # Extract text from all pages
    for i, page in enumerate(doc):
        text = page.get_text()
        pages_text.append((i + 1, text))
        
    doc.close()
    
    # Detect language using first few readable pages
    sample_text = ""
    for _, text in pages_text:
        # Strip spacing and punctuation to see if we have actual word characters
        clean_text = re.sub(r"\s+", " ", text).strip()
        if len(clean_text) > 100:
            sample_text = clean_text[:500]
            break
            
    if not sample_text:
        # Fallback to concatenate all page texts if they are all very short
        sample_text = " ".join([text for _, text in pages_text])
        
    detected_lang = "unknown"
    if sample_text.strip():
        try:
            detected_lang = langdetect.detect(sample_text)
        except LangDetectException:
            pass
            
    # Mismatch check
    if detected_lang != expected_lang and expected_lang in ["hi", "en"]:
        # If detected is 'hi' but expected is 'en' (or vice versa), log warning
        # Sometimes small snippets or numbers make langdetect predict wrong, but let's log warning
        logger.debug(f"Warning: Language mismatch for {os.path.basename(pdf_path)}. Expected '{expected_lang}', detected '{detected_lang}'.")
        
    return pages_text, detected_lang

def _split_into_sentences(text: str) -> list:
    """
    Splits text into language-aware sentences preserving boundary punctuation.
    Supports English (. ? !) and Hindi Devanagari (। \u0964, ॥ \u0965) and double newlines.
    """
    if not text:
        return []
    
    # Normalize carriage returns
    normalized = re.sub(r"\r\n|\r", "\n", text)
    
    # Sentence boundary regex matching text + sentence termination punctuation
    # \u0964 is Devanagari Purna Viram (।), \u0965 is Double Danda (॥)
    pattern = r'([^.!?\u0964\u0965\n]+(?:[.!?\u0964\u0965]+|\n\n|\n|$))'
    raw_parts = re.findall(pattern, normalized)
    
    sentences = []
    for part in raw_parts:
        part_str = part.strip()
        if part_str:
            sentences.append(part_str)
            
    return sentences if sentences else [normalized.strip()]


def chunk_text(pages_text, chunk_size=512, chunk_overlap=80):
    """
    Splits page-by-page text into sentence-aware chunks of target size ~512 characters
    while preserving sentence and paragraph boundaries (English and Hindi Devanagari).
    
    Never cuts a sentence in half. If a single sentence exceeds chunk_size, it is kept as its own chunk.
    Sentence-level overlap retains 1-2 trailing sentences (up to chunk_overlap chars) for the next chunk.
    
    Returns a list of dicts: [{"text": str, "page_number": int, "chunk_index": int}]
    """
    all_chunks = []

    for page_num, text in pages_text:
        if not text or not text.strip():
            continue

        sentences = _split_into_sentences(text)
        if not sentences:
            continue

        chunk_idx = 0
        i = 0

        while i < len(sentences):
            current_sentences = []
            current_len = 0
            start_i = i

            while i < len(sentences):
                sentence = sentences[i]
                sent_len = len(sentence)

                # If single sentence itself is larger than chunk_size and current_chunk is empty,
                # make it its own chunk without force-splitting
                if sent_len >= chunk_size and not current_sentences:
                    current_sentences.append(sentence)
                    i += 1
                    break

                # Check if adding this sentence exceeds chunk_size
                added_len = sent_len + (1 if current_sentences else 0)
                if current_len + added_len > chunk_size and current_sentences:
                    break

                current_sentences.append(sentence)
                current_len += added_len
                i += 1

            chunk_content = " ".join(current_sentences).strip()
            if chunk_content:
                all_chunks.append({
                    "text": chunk_content,
                    "page_number": page_num,
                    "chunk_index": chunk_idx
                })
                chunk_idx += 1

            # Determine sentence overlap for next chunk:
            # Walk backward from i to find trailing sentences up to ~chunk_overlap characters
            if i < len(sentences):
                overlap_len = 0
                overlap_count = 0
                for j in range(i - 1, start_i, -1):
                    s_len = len(sentences[j])
                    if overlap_len + s_len <= chunk_overlap or overlap_count == 0:
                        overlap_len += s_len
                        overlap_count += 1
                    else:
                        break
                # Set next chunk starting sentence index
                i = max(i - overlap_count, start_i + 1)

    return all_chunks

def index_document(domain, language, filename, source_url, discovered_via, file_path):
    """
    Orchestrates extraction, language verification, chunking, embedding generation,
    and storing in ChromaDB + SQLite update.
    Returns (page_count, chunk_count, status).
    """
    try:
        logger.debug(f"Processing PDF for indexing: {filename}...")
        
        # 1. Extract text and language
        pages_text, detected_lang = extract_text_and_language(file_path, language)
        page_count = len(pages_text)
        
        if page_count == 0:
            logger.debug(f"Skipping empty or unreadable PDF: {filename}")
            upsert_document_record(
                domain=domain, language=language, filename=filename, source_url=source_url,
                discovered_via=discovered_via, status="failed", page_count=0, chunk_count=0
            )
            return 0, 0, "failed"
            
        # 2. Chunk text
        chunks = chunk_text(pages_text)
        chunk_count = len(chunks)
        logger.debug(f"Extracted {page_count} pages and created {chunk_count} chunks.")
        
        if chunk_count == 0:
            logger.debug(f"No text chunks created for {filename}.")
            upsert_document_record(
                domain=domain, language=language, filename=filename, source_url=source_url,
                discovered_via=discovered_via, status="failed", page_count=page_count, chunk_count=0
            )
            return page_count, 0, "failed"
            
        # 3. Generate embeddings
        model = get_embedding_model()
        texts = [c["text"] for c in chunks]
        embeddings = model.encode(texts, show_progress_bar=False)
        
        # 4. Insert/Upsert into ChromaDB
        collection = get_chroma_collection()
        
        ids = []
        metadatas = []
        import numpy as np
        
        for idx, chunk in enumerate(chunks):
            # Stable deterministic ID
            chunk_id = f"{filename}_p{chunk['page_number']}_c{chunk['chunk_index']}"
            ids.append(chunk_id)
            
            # Calculate embedding norm
            emb_norm = float(np.linalg.norm(embeddings[idx]))
            
            # Metadata structure
            meta = {
                "domain": domain,
                "language": language,
                "filename": filename,
                "source_url": source_url,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "discovered_via": discovered_via,
                "vector_norm": emb_norm
            }
            metadatas.append(meta)
            
        collection.upsert(
            ids=ids,
            embeddings=[emb.tolist() for emb in embeddings],
            metadatas=metadatas,
            documents=texts
        )
        logger.debug(f"Upserted {chunk_count} chunks into ChromaDB.")
        
        # 5. Update SQLite document record
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        upsert_document_record(
            domain=domain, language=language, filename=filename, source_url=source_url,
            discovered_via=discovered_via, status="indexed", page_count=page_count,
            chunk_count=chunk_count, indexed_at=now_str
        )
        return page_count, chunk_count, "indexed"
        
    except Exception as e:
        logger.debug(f"Error indexing document {filename}: {e}")
        upsert_document_record(
            domain=domain, language=language, filename=filename, source_url=source_url,
            discovered_via=discovered_via, status="failed"
        )
        return 0, 0, "failed"

def get_user_docs_collection():
    """Returns the singleton ChromaDB user_docs collection from services."""
    return services.chroma_manager.get_collection("user_docs")

def get_chroma_client():
    """Returns the singleton ChromaDB client from services."""
    return services.chroma_manager.get_client()

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file using python-docx."""
    doc = docx.Document(docx_path)
    full_text = []
    
    # Extract from paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text)
            
    # Extract from tables
    for table in doc.tables:
        for row in table.rows:
            row_text = []
            for cell in row.cells:
                text_content = cell.text.strip()
                if text_content and text_content not in row_text:
                    row_text.append(text_content)
            if row_text:
                full_text.append(" | ".join(row_text))
                
    return "\n".join(full_text)

def extract_text_from_image_ocr(image_path):
    """
    Robust OCR extraction with DPI upscaling and smart preprocessing
    specifically tuned for scanned medical lab reports and documents.
    Supports PNG, JPG, WEBP, and JPEG image formats.
    """
    from PIL import ImageFilter
    import numpy as np

    try:
        img = Image.open(image_path)
    except Exception as e:
        logger.error(f"Failed to open image for OCR: {e}")
        return "", 0.0

    # 1. Upscale small images to at least 1800px width for better OCR character recognition
    orig_w, orig_h = img.size
    TARGET_W = 1800
    if orig_w < TARGET_W:
        scale = TARGET_W / orig_w
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)

    # 2. Grayscale & Contrast enhancement
    gray = ImageOps.grayscale(img)
    sharpened = gray.filter(ImageFilter.SHARPEN)
    contrasted = ImageOps.autocontrast(sharpened, cutoff=2)

    # 3. Binarization
    img_np = np.array(contrasted)
    mean_val = np.mean(img_np)
    if mean_val > 160:
        threshold = int(mean_val * 0.85)
        processed_img = contrasted.point(lambda p: 255 if p > threshold else 0)
    else:
        processed_img = contrasted

    def _do_pytesseract(image_obj, psm_mode=3, lang="eng+hin"):
        try:
            direct_text = pytesseract.image_to_string(
                image_obj, lang=lang,
                config=f"--oem 3 --psm {psm_mode}"
            ).strip()
        except Exception:
            try:
                direct_text = pytesseract.image_to_string(
                    image_obj, lang="eng",
                    config=f"--oem 3 --psm {psm_mode}"
                ).strip()
            except Exception:
                direct_text = ""

        try:
            data = pytesseract.image_to_data(
                image_obj, lang=lang,
                config=f"--oem 3 --psm {psm_mode}",
                output_type=pytesseract.Output.DICT
            )
        except Exception:
            try:
                data = pytesseract.image_to_data(
                    image_obj, lang="eng",
                    config=f"--oem 3 --psm {psm_mode}",
                    output_type=pytesseract.Output.DICT
                )
            except Exception:
                data = {}

        lines = {}
        confidences = []
        for i in range(len(data.get("text", []))):
            word = (data.get("text", [""])[i] or "").strip()
            conf_raw = data.get("conf", ["-1"])[i]
            try:
                conf = float(conf_raw)
            except Exception:
                conf = -1.0

            if not word:
                continue

            line_key = (
                data.get("page_num", [1])[i],
                data.get("block_num", [0])[i],
                data.get("par_num", [0])[i],
                data.get("line_num", [0])[i],
            )
            lines.setdefault(line_key, []).append(word)
            if conf > 0:
                confidences.append(float(conf))

        sorted_keys = sorted(lines.keys())
        data_text = "\n".join(" ".join(lines[k]) for k in sorted_keys).strip()
        mean_conf_out = sum(confidences) / len(confidences) if confidences else 70.0
        
        # Pick the longer / more complete text between direct string extraction and structured line extraction
        best_text = direct_text if len(direct_text) > len(data_text) else data_text
        return best_text, mean_conf_out

    # Multi-pass OCR: try PSM 3 (auto layout) first, then PSM 6, then PSM 11
    text, mean_conf = _do_pytesseract(processed_img, psm_mode=3)
    if len(text.strip()) < 40:
        text_psm6, conf6 = _do_pytesseract(processed_img, psm_mode=6)
        if len(text_psm6.strip()) > len(text.strip()):
            text, mean_conf = text_psm6, conf6

    # Fallback pass on original image
    if len(text.strip()) < 40:
        raw_text, raw_conf = _do_pytesseract(img, psm_mode=3)
        if len(raw_text.strip()) > len(text.strip()):
            text, mean_conf = raw_text, raw_conf

    # EasyOCR fallback if Tesseract yields under 50 characters
    if len(text.strip()) < 50:
        try:
            import easyocr
            reader = easyocr.Reader(['en', 'hi'], gpu=False)
            results = reader.readtext(image_path)
            easy_lines = [res[1] for res in results if res[2] > 0.15]
            easy_text = "\n".join(easy_lines).strip()
            if len(easy_text) > len(text):
                text = easy_text
                mean_conf = 80.0
        except Exception as ex:
            logger.debug(f"EasyOCR fallback not used: {ex}")

    return text, mean_conf



import hashlib
from metrics_manager import metrics_manager
from job_queue import job_queue
from logger_config import logger
from report_parser import extract_test_results_from_text

def calculate_file_hash(file_path: str) -> str:
    """Computes MD5 hash of a file for duplicate upload checking."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def ingest_user_document_task(
    job_id: str, 
    file_path: str, 
    original_filename: str, 
    session_id: str, 
    domain_hint: str = None, 
    conversation_id: str = None, 
    file_hash: str = None, 
    document_id: str = None
):
    """
    Ingest task executed in background thread pool.
    Updates job status/progress and records performance metrics.
    """
    logger = logging.getLogger("saarthi.jobs")
    ext = os.path.splitext(original_filename)[1].lower()
    ocr_used = ext in {".jpg", ".jpeg", ".png", ".webp"}
    
    try:
        # Step 1: Text Extraction
        job_queue.update_job(job_id, "running", 10, "Extracting Text")
        
        pages_text = []
        detected_lang = "unknown"
        ocr_conf = None
        
        start_extract = time.perf_counter()
        if ext == ".pdf":
            pages_text, detected_lang = extract_text_and_language(file_path, "unknown")
            has_text = any(t.strip() for _, t in pages_text)
            
            if not has_text:
                logger.info(f"No text extracted via fitz for {file_path}. Falling back to OCR...")
                ocr_used = True
                
                doc = fitz.open(file_path)
                pages_text = []
                confidences = []
                
                for i, page in enumerate(doc):
                    pix = page.get_pixmap(dpi=150)
                    temp_img_path = f"{file_path}_page_{i}.png"
                    pix.save(temp_img_path)
                    
                    try:
                        text, conf = extract_text_from_image_ocr(temp_img_path)
                        from ocr_sanitizer import ocr_sanitizer
                        text = ocr_sanitizer.sanitize_ocr_text(text)
                        
                        pages_text.append((i + 1, text))
                        if conf > 0:
                            confidences.append(conf)
                    finally:
                        if os.path.exists(temp_img_path):
                            try:
                                os.remove(temp_img_path)
                            except:
                                pass
                
                doc.close()
                if confidences:
                    ocr_conf = sum(confidences) / len(confidences)
                else:
                    ocr_conf = 0.0
                    
        elif ext == ".docx":
            text = extract_text_from_docx(file_path)
            pages_text = [(1, text)]
        else: # Images
            text, ocr_conf = extract_text_from_image_ocr(file_path)
            from ocr_sanitizer import ocr_sanitizer
            text = ocr_sanitizer.sanitize_ocr_text(text)
            pages_text = [(1, text)]
            
        extract_time = time.perf_counter() - start_extract
        if ocr_used:
            metrics_manager.record("ocr_time", extract_time)
            
        page_count = len(pages_text)
        has_text = any(t.strip() for _, t in pages_text)
        if not has_text:
            raise ValueError("No readable text found in document")

        # If this looks like a medical lab report, parse structured test results
        try:
            # Collect per-page parsed results and, if found, prepend a structured summary chunk
            structured_blocks = []
            for pnum, ptext in pages_text:
                parsed = extract_test_results_from_text(ptext)
                if parsed:
                    # Build a readable structured summary
                    lines = [f"{r['test_name']} → {r['result']}" for r in parsed]
                    structured = "Structured Test Results:\n" + "\n".join(lines)
                    structured_blocks.append((pnum, structured))

            # If we found any structured results, insert a leading page with aggregated facts
            if structured_blocks:
                agg_lines = []
                for _, block in structured_blocks:
                    agg_lines.append(block)
                agg_text = "\n\n".join(agg_lines)
                # Prepend as page 0 so chunking and prompts include it first
                pages_text.insert(0, (0, agg_text))
                page_count = len(pages_text)
        except Exception:
            # Non-fatal parsing errors shouldn't stop indexing
            pass
            
        if ext in {".docx", ".jpg", ".jpeg", ".png", ".webp"}:
            sample_text = ""
            for _, t in pages_text:
                clean_t = re.sub(r"\s+", " ", t).strip()
                if len(clean_t) > 100:
                    sample_text = clean_t[:500]
                    break
            if not sample_text:
                sample_text = " ".join([t for _, t in pages_text])
            if sample_text.strip():
                try:
                    detected_lang = langdetect.detect(sample_text)
                except Exception:
                    pass

        # Step 2: Chunking
        job_queue.update_job(job_id, "running", 40, "Chunking Text")
        chunks = chunk_text(pages_text)
        chunk_count = len(chunks)
        if chunk_count == 0:
            raise ValueError("Document could not be chunked")

        # Step 3: Embeddings
        job_queue.update_job(job_id, "running", 60, "Generating Embeddings")
        
        start_embed = time.perf_counter()
        # Use singleton embedding service
        model = get_embedding_model()
        texts = [c["text"] for c in chunks]
        embeddings = model.encode(texts, show_progress_bar=False)
        embed_time = time.perf_counter() - start_embed
        metrics_manager.record("embedding_time", embed_time)

        # Step 4: Vector Indexing
        job_queue.update_job(job_id, "running", 80, "Indexing Vectors")
        collection = get_user_docs_collection()
        ids = []
        metadatas = []
        import numpy as np
        
        from ocr_sanitizer import ocr_sanitizer

        for idx, chunk in enumerate(chunks):
            chunk_id = f"{session_id}_{document_id}_p{chunk['page_number']}_c{chunk['chunk_index']}"
            ids.append(chunk_id)
            
            # Calculate embedding norm
            emb_norm = float(np.linalg.norm(embeddings[idx]))

            # Assess chunk OCR quality score
            quality_assessment = ocr_sanitizer.assess_ocr_quality(chunk["text"])
            quality_score = quality_assessment["quality_score"]

            if quality_assessment["is_low_quality"]:
                logger.warning(
                    f"Low OCR quality score ({quality_score}) for '{original_filename}' "
                    f"on page {chunk['page_number']}. Warnings: {quality_assessment['warnings']}"
                )

            meta = {
                "session_id": session_id,
                "conversation_id": conversation_id or "",
                "document_id": document_id,
                "original_filename": original_filename,
                "file_type": ext,
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"],
                "language": detected_lang,
                "vector_norm": emb_norm,
                "ocr_quality_score": quality_score
            }
            if domain_hint:
                meta["domain_hint"] = domain_hint
            metadatas.append(meta)

            
        collection.upsert(
            ids=ids,
            embeddings=[emb.tolist() for emb in embeddings],
            metadatas=metadatas,
            documents=texts
        )
        
        ocr_confidence = ocr_conf if ocr_used else None
        ocr_low_quality_warning = (ocr_confidence < OCR_LOW_CONFIDENCE_THRESHOLD) if ocr_used else False
        
        # Step 5: Finalize status records
        session_manager.update_document_status(
            document_id=document_id,
            session_id=session_id,
            status="indexed",
            page_count=page_count,
            chunk_count=chunk_count,
            ocr_confidence=ocr_confidence,
            ocr_low_quality_warning=ocr_low_quality_warning
        )
        
        job_queue.update_job(job_id, "completed", 100, "Ready")
        
    except Exception as e:
        logger.error(f"Error in background ingestion job {job_id}: {e}")
        try:
            current_ocr_conf = ocr_conf
        except NameError:
            current_ocr_conf = None
            
        ocr_low_quality = (current_ocr_conf < OCR_LOW_CONFIDENCE_THRESHOLD) if current_ocr_conf is not None else False
        
        session_manager.update_document_status(
            document_id=document_id,
            session_id=session_id,
            status="failed",
            ocr_confidence=current_ocr_conf,
            ocr_low_quality_warning=ocr_low_quality
        )
        
        job_queue.update_job(job_id, "failed", 100, "Failed", error_message=str(e))
        
    finally:
        # Guarantee cleanup of temporary uploads
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Purged temporary ingestion file: {file_path}")
            except Exception as cleanup_err:
                logger.error(f"Failed to delete temp file {file_path}: {cleanup_err}")

def ingest_user_document(file_path, original_filename, session_id, domain_hint=None, conversation_id=None):
    """
    Synchronous compat wrapper for legacy caller interfaces.
    Launches and awaits the pipeline synchronously.
    """
    ext = os.path.splitext(original_filename)[1].lower()
    document_id = f"doc_{uuid.uuid4().hex}"
    
    session_manager.create_document_record(
        document_id=document_id,
        session_id=session_id,
        original_filename=original_filename,
        file_type=ext,
        domain_hint=domain_hint,
        ocr_used=ext in {".jpg", ".jpeg", ".png", ".webp"},
        status="pending",
        conversation_id=conversation_id
    )
    
    job_id = job_queue.create_job(document_id, conversation_id)
    ingest_user_document_task(
        job_id, file_path, original_filename, session_id, 
        domain_hint, conversation_id, None, document_id
    )
    
    # Return compatibility format
    doc_record = session_manager.get_document_record(document_id, session_id)
    return {
        "document_id": document_id,
        "ocr_confidence": doc_record.get("ocr_confidence"),
        "ocr_low_quality_warning": doc_record.get("ocr_low_quality_warning"),
        "message": "Ingestion task finished."
    }

def delete_document_and_chunks(document_id, session_id):
    """
    Validates ownership, hard-deletes vectors from ChromaDB,
    and soft-deletes the SQLite metadata row (sets status='deleted').
    """
    # Verify ownership
    doc_record = session_manager.get_document_record(document_id, session_id)
    if not doc_record:
        raise ValueError("Document not found or does not belong to this session")
        
    # Hard-delete chunks from ChromaDB
    collection = get_user_docs_collection()
    collection.delete(where={"document_id": document_id})
    logger.debug(f"Hard-deleted chunks for document {document_id} from ChromaDB.")
    
    # Soft-delete record in SQLite
    session_manager.delete_document_record(document_id, session_id)
    logger.debug(f"Soft-deleted document record {document_id} in SQLite.")

def parse_markdown_file(file_path: str):
    """
    Parses a markdown file to extract frontmatter (YAML) and content body.
    Returns metadata dict and content body string.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        
    meta = {}
    content = text
    
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_meta = parts[1]
            content = parts[2]
            for line in raw_meta.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip("[]").strip('"').strip("'")
                    meta[k] = v

    return meta, content.strip()

def index_all_local_knowledge_base():
    """
    Recursively scans the local knowledge_base directory
    and indexes all .md, .txt, and .pdf files into ChromaDB's knowledge_base collection.
    """
    import numpy as np
    import services
    
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(backend_dir)
    
    kb_root_candidates = [
        os.path.join(workspace_root, "knowledge_base"),
        os.path.join(backend_dir, "data", "knowledge_base"),
        "./knowledge_base"
    ]
    
    kb_root = None
    for cand in kb_root_candidates:
        if os.path.isdir(cand):
            kb_root = cand
            break
            
    if not kb_root:
        logger.warning("No local knowledge_base directory found for indexing.")
        return 0

    logger.info(f"Indexing local knowledge base files from: {kb_root}")
    
    collection = services.chroma_manager.get_collection("knowledge_base")
    model = get_embedding_model()
    
    total_indexed_files = 0
    total_chunks_added = 0
    
    batch_ids = []
    batch_embeddings = []
    batch_metadatas = []
    batch_documents = []
    
    for root, dirs, files in os.walk(kb_root):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in [".md", ".txt"]:
                continue
                
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, kb_root)
            path_parts = rel_path.split(os.sep)
            
            # Determine domain hint from parent folder (e.g. medical, banking, legal, common)
            domain = "common"
            if len(path_parts) > 1:
                top_folder = path_parts[0].lower()
                if top_folder in ["medical", "hospital", "symptoms", "medicines"]:
                    domain = "medical"
                elif top_folder in ["banking"]:
                    domain = "banking"
                elif top_folder in ["legal", "constitution"]:
                    domain = "legal"
                    
            if ext in [".md", ".txt"]:
                meta, body = parse_markdown_file(file_path)
                
                if meta.get("domain"):
                    doc_domain = meta.get("domain").lower()
                    if doc_domain in ["medical", "hospital"]:
                        domain = "medical"
                    elif doc_domain in ["banking"]:
                        domain = "banking"
                    elif doc_domain in ["legal", "constitution", "constitution_and_general_law"]:
                        domain = "legal"
                        
                title = meta.get("title") or os.path.splitext(file)[0].replace("_", " ").title()
                keywords = meta.get("keywords") or meta.get("aliases") or ""
                category = meta.get("category") or "general"
                
                # Split body into logical chunks
                paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
                current_chunk = f"Title: {title}\nKeywords: {keywords}\n"
                chunks = []
                
                for para in paragraphs:
                    if len(current_chunk) + len(para) < 750:
                        current_chunk += "\n" + para
                    else:
                        chunks.append(current_chunk)
                        current_chunk = f"Title: {title} (Contd)\nKeywords: {keywords}\n" + para
                if current_chunk.strip():
                    chunks.append(current_chunk)
                    
                if not chunks:
                    continue
                    
                embeddings = model.encode(chunks, show_progress_bar=False)
                
                for idx, chunk_text in enumerate(chunks):
                    chunk_id = f"kb_md_{hashlib.md5(rel_path.encode('utf-8')).hexdigest()[:10]}_c{idx}"
                    emb_norm = float(np.linalg.norm(embeddings[idx]))
                    
                    meta_dict = {
                        "domain": domain,
                        "category": category,
                        "title": title,
                        "filename": file,
                        "source": rel_path.replace(os.sep, "/"),
                        "source_url": rel_path.replace(os.sep, "/"),
                        "language": "multilingual",
                        "page_number": 1,
                        "chunk_index": idx,
                        "vector_norm": emb_norm
                    }
                    
                    batch_ids.append(chunk_id)
                    batch_embeddings.append(embeddings[idx].tolist())
                    batch_metadatas.append(meta_dict)
                    batch_documents.append(chunk_text)
                    
                    if len(batch_ids) >= 100:
                        collection.upsert(
                            ids=batch_ids,
                            embeddings=batch_embeddings,
                            metadatas=batch_metadatas,
                            documents=batch_documents
                        )
                        total_chunks_added += len(batch_ids)
                        batch_ids, batch_embeddings, batch_metadatas, batch_documents = [], [], [], []
                        
                total_indexed_files += 1

    if batch_ids:
        collection.upsert(
            ids=batch_ids,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas,
            documents=batch_documents
        )
        total_chunks_added += len(batch_ids)

    logger.info(f"Local Markdown KB indexing complete! Indexed {total_indexed_files} files ({total_chunks_added} chunks).")
    return total_chunks_added

