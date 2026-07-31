import os
import sys
import sqlite3
import numpy as np

# Ensure workspace is in import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import kb_pipeline
import session_manager
from glossary.query_expander import expand_query_with_glossary

# Configuration
MIN_SIMILARITY_SCORE = 0.25
USER_DOC_MIN_SIMILARITY = 0.25

# Hinglish -> English medical term normalization map
# Ensures correct retrieval even when user writes in Hinglish romanization
HINGLISH_MEDICAL_MAP = {
    "pet dard": "stomach pain abdominal pain",
    "pet drd": "stomach pain abdominal pain",
    "pet me dard": "stomach pain abdominal pain",
    "pait dard": "stomach pain abdominal pain",
    "pet me jalan": "stomach burning acidity gastritis",
    "bukhar": "fever temperature",
    "bhukar": "fever temperature",
    "khansi": "cough respiratory",
    "ulti": "vomiting nausea",
    "sir dard": "headache migraine",
    "seena dard": "chest pain cardiac",
    "dawa": "medicine medication",
    "dawai": "medicine medication",
    "dva": "medicine medication",
    "dvai": "medicine medication",
    "ilaj": "treatment therapy",
    "bimari": "disease illness condition",
    "lakshan": "symptoms signs",
}

def normalize_hinglish_query(query: str) -> str:
    """Expands Hinglish medical terms in query with their English equivalents for better retrieval."""
    q_lower = query.lower()
    expanded = q_lower
    for hindi_term, english_equiv in HINGLISH_MEDICAL_MAP.items():
        if hindi_term in q_lower:
            expanded = expanded + " " + english_equiv
    return expanded.strip()

def check_session_exists(session_id: str) -> bool:
    """Validates that a session_id actually exists in SQLite user_sessions."""
    if not session_id:
        return False
    conn = session_manager.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM user_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def process_results(query_results: dict, collection_name: str, norm_q: float) -> list:
    """
    Processes, filters, and normalizes ChromaDB query results.
    Computes exact Cosine Similarity from squared L2 distance and vector norms (stored in metadata to avoid slow DB reads).
    """
    chunks = []
    if not query_results or not query_results.get('ids') or len(query_results['ids'][0]) == 0:
        return chunks
        
    ids = query_results['ids'][0]
    distances = query_results['distances'][0]
    metadatas = query_results['metadatas'][0]
    documents = query_results['documents'][0]
    
    for i in range(len(ids)):
        dist = distances[i]
        meta = metadatas[i]
        
        # Read pre-calculated norm from metadata, or fallback to average norm (2.5) if not indexed yet
        norm_db = float(meta.get("vector_norm", 2.5))
        
        # Exact Cosine Similarity formula using norms and squared L2 distance:
        # L2_dist = ||q||^2 + ||db||^2 - 2 * ||q|| * ||db|| * cos_sim
        # => cos_sim = (||q||^2 + ||db||^2 - L2_dist) / (2 * ||q|| * ||db||)
        if norm_q > 0 and norm_db > 0:
            sim = (norm_q**2 + norm_db**2 - dist) / (2.0 * norm_q * norm_db)
        else:
            sim = 0.0
            
        required_threshold = USER_DOC_MIN_SIMILARITY if collection_name == "user_docs" else MIN_SIMILARITY_SCORE
        if sim >= required_threshold:
            filename = meta.get('filename') or meta.get('original_filename') or 'unknown'
            domain = meta.get('domain') or meta.get('domain_hint') or 'user_upload'
            language = meta.get('language') or 'en'
            page_num = meta.get('page_number') or 1
            
            chunks.append({
                "text": documents[i],
                "source": filename,
                "domain": domain,
                "language": language,
                "page_number": page_num,
                "collection": collection_name,
                "similarity_score": sim
            })
            
    return chunks

def is_document_about_query(query: str) -> bool:
    """
    Detects trigger phrases indicating the user wants to ask about or summarize their uploaded document.
    """
    if not query:
        return False
    query_lower = query.lower()
    trigger_phrases = [
        "pdf", "document", "uploaded file", "is file", "jo upload",
        "summary", "samjhao", "explain", "kya hai", "kya likha",
        "summarize", "summarise", "about this", "brief", "reprort",
        "repot", "report", "mera document", "uploaded", "my file", 
        "this doc", "this file", "analyze", "analyse", "overview",
        "check", "batao", "read", "describe", "details", "extract"
    ]
    return any(phrase in query_lower for phrase in trigger_phrases)


def force_retrieve_user_doc_chunks(session_id: str, conversation_id: str = None, n: int = 6) -> list:
    """
    Queries user_docs ChromaDB collection with where filter matching session and conversation
    and NO query embedding. Orders results by page_number and chunk_index.
    Returns the first n chunks as context, each with similarity_score=1.0.
    """
    collection = kb_pipeline.get_user_docs_collection()
    where_filter = {"session_id": session_id}
    if conversation_id:
        where_filter = {"$and": [{"session_id": session_id}, {"conversation_id": conversation_id}]}
    results = collection.get(
        where=where_filter,
        include=["metadatas", "documents"]
    )
    
    chunks = []
    if not results or not results.get('ids') or len(results['ids']) == 0:
        return chunks
        
    metadatas = results.get('metadatas', [])
    documents = results.get('documents', [])
    
    for i in range(len(results['ids'])):
        meta = metadatas[i]
        text = documents[i]
        filename = meta.get('original_filename') or meta.get('filename') or 'unknown'
        domain = meta.get('domain_hint') or meta.get('domain') or 'user_upload'
        language = meta.get('language') or 'en'
        page_num = meta.get('page_number') or 1
        chunk_index = meta.get('chunk_index') or 0
        
        chunks.append({
            "text": text,
            "source": filename,
            "domain": domain,
            "language": language,
            "page_number": page_num,
            "chunk_index": chunk_index,
            "collection": "user_docs",
            "similarity_score": 1.0
        })
        
    # Sort results by page_number, then chunk_index to make a coherent layout
    chunks = sorted(chunks, key=lambda x: (x["page_number"], x.get("chunk_index", 0)))
    return chunks[:n]

def retrieve_context(query: str, session_id: str | None, conversation_id: str | None = None, query_language: str = None, query_domain: str = None) -> dict:
    """
    Exposes primary RAG retrieval interface.
    1. Expands incoming query using glossary.
    2. Generates multilingual embeddings.
    3. Retrieves from user_docs and knowledge_base.
    4. Filters results by MIN_SIMILARITY_SCORE using exact Cosine Similarity.
    5. Prioritizes user_docs over knowledge_base.
    6. Returns up to 10 final context chunks.
    """
    session_valid = check_session_exists(session_id)
    
    # Check if this is a document summary/explanation request and the session has documents
    if session_valid and is_document_about_query(query):
        docs = session_manager.get_session_documents(session_id, conversation_id=conversation_id)
        if docs:
            forced_chunks = force_retrieve_user_doc_chunks(session_id, conversation_id, n=6)
            if forced_chunks:
                return {
                    "expanded_query": expand_query_with_glossary(query),
                    "context_chunks": forced_chunks,
                    "user_doc_chunks_used": len(forced_chunks),
                    "knowledge_base_chunks_used": 0,
                    "has_any_context": True,
                    "forced_user_doc_retrieval": True
                }

    # 1. Expand query via Stage 0 Glossary + Hinglish normalization
    expanded_query = expand_query_with_glossary(query)
    expanded_query = normalize_hinglish_query(expanded_query)  # Expand Hinglish medical terms
    
    # 2. Generate embedding using shared model singleton
    model = kb_pipeline.get_embedding_model()
    query_emb_np = model.encode(expanded_query)
    norm_q = float(np.linalg.norm(query_emb_np))
    query_embedding = query_emb_np.tolist()
    
    # 3. Retrieve from user_docs if session exists
    user_chunks = []
    
    if session_valid:
        user_collection = kb_pipeline.get_user_docs_collection()
        where_filter = {"session_id": session_id}
        if conversation_id:
            where_filter = {"$and": [{"session_id": session_id}, {"conversation_id": conversation_id}]}
        # Retrieve up to top_k = 8
        results_user = user_collection.query(
            query_embeddings=[query_embedding],
            n_results=8,
            where=where_filter,
            include=["metadatas", "documents", "distances"]
        )
        user_chunks = process_results(results_user, "user_docs", norm_q)
        
        # User Doc Topic Filter (Fix 1 Addendum):
        # If this is not an explicit document summary query, exclude weak user document chunks (similarity < 0.50)
        # to prevent unrelated uploads from appearing in general queries.
        if not is_document_about_query(query):
            user_chunks = [c for c in user_chunks if c["similarity_score"] >= 0.50]
        
    # 4. Retrieve from knowledge_base with domain filtering
    query_lower = query.lower()
    med_terms = ["cancer", "blood", "leukemia", "prostate", "tumor", "fever", "bukhar", "pain", "dard", "drd", "bimari", "doctor", "hospital", "dawa", "dawai", "dvai", "dva", "medicine", "symptoms", "laksan", "lakshan", "ilaj", "treatment", "report", "vomit", "cough", "khansi"]
    bank_terms = ["bank", "kyc", "account", "loan", "interest", "rbi", "card", "khata", "paisa", "atm", "transaction", "foreclosure"]
    leg_terms = ["court", "ipc", "crpc", "bnss", "fir", "police", "rti", "complaint", "vakeel", "dhara", "kanoon", "law", "rights", "constitution"]

    is_med_query = (query_domain == "Medical") or any(k in query_lower for k in med_terms)
    is_bank_query = (query_domain == "Banking") or any(k in query_lower for k in bank_terms)
    is_leg_query = (query_domain == "Legal") or any(k in query_lower for k in leg_terms)

    where_clause = None
    if is_med_query and not (is_bank_query or is_leg_query):
        where_clause = {"domain": {"$in": ["hospital", "medical", "common"]}}
    elif is_bank_query and not (is_med_query or is_leg_query):
        where_clause = {"domain": "banking"}
    elif is_leg_query and not (is_med_query or is_bank_query):
        where_clause = {"domain": {"$in": ["legal", "constitution_and_general_law"]}}

    kb_chunks = []
    kb_collection = kb_pipeline.get_chroma_collection()
    
    try:
        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": 25,
            "include": ["metadatas", "documents", "distances"]
        }
        if where_clause:
            query_kwargs["where"] = where_clause

        results_global = kb_collection.query(**query_kwargs)
        kb_chunks = process_results(results_global, "knowledge_base", norm_q)
    except Exception:
        try:
            results_global = kb_collection.query(
                query_embeddings=[query_embedding],
                n_results=25,
                include=["metadatas", "documents", "distances"]
            )
            kb_chunks = process_results(results_global, "knowledge_base", norm_q)
        except Exception:
            kb_chunks = []

    # Strict domain isolation: purge cross-domain chunks
    if is_med_query and not (is_bank_query or is_leg_query):
        kb_chunks = [c for c in kb_chunks if "constitution" not in c.get("source", "").lower() and "banking" not in c.get("source", "").lower() and c.get("domain") not in ("banking", "legal", "constitution_and_general_law")]
    elif is_bank_query and not (is_med_query or is_leg_query):
        kb_chunks = [c for c in kb_chunks if "medical" not in c.get("source", "").lower() and "hospital" not in c.get("source", "").lower() and c.get("domain") not in ("medical", "hospital", "legal")]
    elif is_leg_query and not (is_med_query or is_bank_query):
        kb_chunks = [c for c in kb_chunks if "banking" not in c.get("source", "").lower() and "medical" not in c.get("source", "").lower() and c.get("domain") not in ("medical", "hospital", "banking")]

    # Cancer & Blood Cancer specific boost
    if "cancer" in query_lower or "leukemia" in query_lower:
        for chunk in kb_chunks:
            txt_lower = chunk["text"].lower()
            if "cancer" in txt_lower or "leukemia" in txt_lower or "tumor" in txt_lower:
                chunk["similarity_score"] += 0.40
            if "symptom" in txt_lower or "blood" in txt_lower:
                chunk["similarity_score"] += 0.20
                
    # RTI Boost
    if any(k in query_lower for k in ["rti", "right to information", "सूचना का अधिकार", "suchna ka adhikar"]):
        for chunk in kb_chunks:
            if "rti" in chunk["source"].lower() or "information" in chunk["source"].lower():
                chunk["similarity_score"] += 0.35
                
    # KYC Boost
    if "kyc" in query_lower:
        for chunk in kb_chunks:
            if "kyc" in chunk["source"].lower():
                chunk["similarity_score"] += 0.35
                
    # Consumer Protection Boost
    if any(k in query_lower for k in ["consumer", "upbhokta", "उपभोक्ता", "shikayat", "complaint"]):
        for chunk in kb_chunks:
            if "consumer" in chunk["source"].lower():
                chunk["similarity_score"] += 0.35

    # Stomach pain / Abdominal pain / General symptom boost & isolation
    is_pain_or_fever = any(k in query_lower for k in ["pet", "drd", "dard", "stomach", "pain", "bukhar", "bhukar", "fever", "bcha", "bacha", "child", "vomit", "ulti", "dva", "dawai", "goli", "upchar", "symptom"])
    is_sexual_query = any(k in query_lower for k in ["sex", "condom", "youn", "timing", "bdhaye", "pehna", "libido", "erectile", "masturbation"])

    if is_pain_or_fever and not is_sexual_query:
        for chunk in kb_chunks:
            src_lower = chunk["source"].lower()
            txt_lower = chunk["text"].lower()
            if any(k in query_lower for k in ["pet", "stomach", "abdominal"]) and any(k in src_lower or k in txt_lower for k in ["stomach", "abdominal", "pet"]):
                chunk["similarity_score"] += 0.55
            elif "symptoms" in src_lower or "pain" in src_lower:
                chunk["similarity_score"] += 0.45
        kb_chunks = [c for c in kb_chunks if "sexual_health" not in c["source"].lower()]


    # Sexual Health Boost
    if is_sexual_query:
        for chunk in kb_chunks:
            src_lower = chunk["source"].lower()
            if "sexual" in src_lower or "reproductive" in src_lower or "health" in src_lower or "family" in src_lower:
                chunk["similarity_score"] += 0.35
            if "masturbation" in query_lower and "masturbation" in src_lower:
                chunk["similarity_score"] += 0.45

    # 4.6 Language-aware filtering for KB chunks
    if query_language:
        if query_language == "English":
            lang_filtered = [c for c in kb_chunks if "_hi" not in c["source"].lower().split(".")[0][-3:]]
        elif query_language == "Hindi":
            lang_filtered = [c for c in kb_chunks if "_en" not in c["source"].lower().split(".")[0][-3:]]
        elif query_language == "Hinglish":
            for chunk in kb_chunks:
                if "hinglish:" in chunk["text"].lower() or "hinglish" in chunk["text"].lower():
                    chunk["similarity_score"] += 0.25
            lang_filtered = kb_chunks
        else:
            lang_filtered = kb_chunks
        
        if lang_filtered:
            kb_chunks = lang_filtered

    # 5. Boost local knowledge_base chunks (from internal MD files) over external ICMR/NHM sources
    # Internal KB md files should be the FIRST priority knowledge source
    for chunk in kb_chunks:
        src_lower = chunk.get("source", "").lower()
        # If source is a local .md file from our knowledge_base folders, boost it
        if src_lower.endswith(".md") or src_lower.endswith(".txt"):
            chunk["similarity_score"] += 0.15
        # Slightly de-prioritize external ICMR/government download sources when local content exists
        elif any(ext in src_lower for ext in ["icmr", "nhm", "mohfw", "who", "niti"]):
            chunk["similarity_score"] -= 0.05

    # 6. Merge and rank
    # Sort each set descending by similarity score
    user_chunks = sorted(user_chunks, key=lambda x: x["similarity_score"], reverse=True)
    kb_chunks = sorted(kb_chunks, key=lambda x: x["similarity_score"], reverse=True)
    
    # Tiered ranking: user_docs has absolute priority
    # If user has uploaded documents, cap knowledge base chunks to prevent drowning the user document context.
    if len(user_chunks) > 0:
        kb_chunks = kb_chunks[:3]
        
    merged_chunks = user_chunks + kb_chunks
    
    # Cap total context chunks to 5
    final_chunks = merged_chunks[:5]
    
    # Usage metrics
    user_docs_used = sum(1 for c in final_chunks if c["collection"] == "user_docs")
    kb_used = sum(1 for c in final_chunks if c["collection"] == "knowledge_base")
    
    has_any_context = len(final_chunks) > 0
    
    return {
        "expanded_query": expanded_query,
        "context_chunks": final_chunks,
        "user_doc_chunks_used": user_docs_used,
        "knowledge_base_chunks_used": kb_used,
        "has_any_context": has_any_context
    }
