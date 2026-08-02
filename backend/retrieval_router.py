import os
import sys
import sqlite3
import numpy as np


# Ensure workspace is in import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import kb_pipeline
import session_manager
from intent_service import intent_service
from glossary.query_expander import expand_query_with_glossary

def classify_domain(query: str):
    res = intent_service.classify_query(query)
    return res.get("domain", "General"), res.get("confidence_score", 0.7)


# Configuration
MIN_SIMILARITY_SCORE = 0.15
USER_DOC_MIN_SIMILARITY = 0.15


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

# ---------------------------------------------------------------------------
# RETRIEVAL INTENT CLASSIFICATION FOR USER DOCUMENTS:
# 1. Whole-Document Summary Intent: The user explicitly requests an overview/summary of the entire uploaded file.
#    In this case, we bypass single-chunk semantic search and retrieve document chunks sequentially across the
#    FULL length of the document (sorted by page order up to an expanded budget n=25).
# 2. Specific Fact Retrieval Intent: The user asks a targeted question (e.g., "doctor name", "receipt number").
#    In this case, we ALWAYS run semantic vector embedding search against user_docs so ChromaDB dynamically
#    retrieves relevant chunks from ANY page (including pages 2, 3, 4, 5+). Only if semantic search returns
#    zero results do we fall back to sequential first-N chunk retrieval.
# ---------------------------------------------------------------------------

TRUE_SUMMARY_TRIGGERS = [
    "summary", "summarize", "summarise", "overview", "briefing", "brief my report",
    "brief report", "poora document samjhao", "explain this document", "explain my report",
    "explain report", "report explain", "full report", "entire document", "full summary",
    "overall report", "report brief"
]

def is_whole_document_summary_query(query: str) -> bool:
    """Detects if query explicitly requests a full overview/summary of the uploaded document."""
    if not query:
        return False
    q_lower = query.lower()
    return any(phrase in q_lower for phrase in TRUE_SUMMARY_TRIGGERS)

def is_document_about_query(query: str) -> bool:
    """Detects trigger phrases indicating the user is asking about or summarizing their uploaded document."""
    if not query:
        return False
    q_lower = query.lower()
    doc_mentions = [
        "pdf", "document", "uploaded file", "is file", "jo upload", "report",
        "mera document", "uploaded", "my file", "this doc", "this file",
        "in the pdf", "in the document", "file me", "doc me", "pdf me"
    ]
    return is_whole_document_summary_query(query) or any(phrase in q_lower for phrase in doc_mentions)


def force_retrieve_user_doc_chunks(
    session_id: str,
    conversation_id: str = None,
    document_ids: list[str] = None,
    n: int = 25,
) -> list:
    """
    Queries user_docs ChromaDB collection with where filter matching session and conversation
    and NO query embedding. Orders results by page_number and chunk_index.
    Returns up to n chunks as context in page order (default n=25 covers full multi-page documents).
    """
    collection = kb_pipeline.get_user_docs_collection()
    where_filter = {"session_id": session_id}
    results = collection.get(
        where=where_filter,
        include=["metadatas", "documents"]
    )
    
    chunks = []
    if not results or not results.get('ids') or len(results['ids']) == 0:
        return chunks
        
    metadatas = results.get('metadatas', [])
    documents = results.get('documents', [])
    
    allowed_document_ids = set(document_ids or [])

    for i in range(len(results['ids'])):
        meta = metadatas[i]
        text = documents[i]
        filename = meta.get('original_filename') or meta.get('filename') or 'unknown'
        domain = meta.get('domain_hint') or meta.get('domain') or 'user_upload'
        language = meta.get('language') or 'en'
        page_num = meta.get('page_number') or 1
        chunk_index = meta.get('chunk_index') or 0
        document_id = meta.get('document_id')

        if allowed_document_ids and document_id and document_id not in allowed_document_ids:
            continue
        
        chunks.append({
            "text": text,
            "source": filename,
            "domain": domain,
            "language": language,
            "page_number": page_num,
            "chunk_index": chunk_index,
            "document_id": document_id,
            "collection": "user_docs",
            "similarity_score": 1.0
        })
        
    # Sort results by page_number, then chunk_index to make a coherent layout
    chunks = sorted(chunks, key=lambda x: (x["page_number"], x.get("chunk_index", 0)))
    return chunks[:n]

def _get_latest_session_document_ids(session_id: str, conversation_id: str = None) -> list:
    """Returns the most recently uploaded non-deleted document IDs for a session."""
    docs = session_manager.get_session_documents(session_id, conversation_id=conversation_id)
    if not docs:
        return []

    docs = sorted(docs, key=lambda d: d.get("uploaded_at") or "", reverse=True)
    return [docs[0].get("id")] if docs[0].get("id") else []

def retrieve_context(query: str, session_id: str | None, conversation_id: str | None = None, query_language: str = None, query_domain: str = None) -> dict:
    """
    Exposes primary RAG retrieval interface.
    1. Expands incoming query using glossary.
    2. Generates multilingual embeddings.
    3. Retrieves from user_docs (strictly scoped to active conversation) and knowledge_base.
    4. Filters results using exact Cosine Similarity and local .md file priority.
    """
    session_valid = check_session_exists(session_id)
    
    # Check if the ACTIVE conversation has uploaded documents
    active_conv_docs = []
    if session_valid and conversation_id:
        active_conv_docs = session_manager.get_session_documents(session_id, conversation_id=conversation_id)

    # 1. WHOLE-DOCUMENT SUMMARY INTENT:
    # If user explicitly requests a full document summary (e.g. "explain my report", "summary do"),
    # force sequential retrieval across ALL pages (n=25 chunks) in page order.
    if session_valid and (active_conv_docs or is_document_about_query(query)) and is_whole_document_summary_query(query):
        doc_ids_to_use = [d["id"] for d in active_conv_docs if d.get("id")]
        if not doc_ids_to_use:
            doc_ids_to_use = _get_latest_session_document_ids(session_id, conversation_id=conversation_id)

        if doc_ids_to_use:
            forced_chunks = force_retrieve_user_doc_chunks(
                session_id,
                conversation_id=conversation_id,
                document_ids=doc_ids_to_use,
                n=25,  # Full document sequential coverage
            )
            if forced_chunks:
                return {
                    "expanded_query": expand_query_with_glossary(query),
                    "context_chunks": forced_chunks,
                    "user_doc_chunks_used": len(forced_chunks),
                    "knowledge_base_chunks_used": 0,
                    "has_any_context": True,
                    "forced_user_doc_retrieval": True
                }

    # 2. SPECIFIC FACT RETRIEVAL INTENT (OR GENERAL QA):
    # For specific questions (e.g., "doctor name", "billing amount page 4"), DO NOT force first-N chunks.
    # Perform semantic embedding search against user_docs so ChromaDB retrieves relevant chunks from ANY page.

    # 1. Expand query via Stage 0 Glossary + Hinglish normalization
    expanded_query = expand_query_with_glossary(query)
    expanded_query = normalize_hinglish_query(expanded_query)  # Expand Hinglish medical terms
    
    # 2. Generate embedding using shared model singleton
    model = kb_pipeline.get_embedding_model()
    query_emb_np = model.encode(expanded_query)
    norm_q = float(np.linalg.norm(query_emb_np))
    query_embedding = query_emb_np.tolist()
    
    # 3. Retrieve from user_docs ONLY IF active conversation has uploaded documents
    user_chunks = []
    
    if session_valid and active_conv_docs:
        user_collection = kb_pipeline.get_user_docs_collection()
        where_conditions = [{"session_id": session_id}]
        if conversation_id:
            where_conditions.append({"conversation_id": conversation_id})
        where_filter = {"$and": where_conditions} if len(where_conditions) > 1 else where_conditions[0]

        results_user = user_collection.query(
            query_embeddings=[query_embedding],
            n_results=8,
            where=where_filter,
            include=["metadatas", "documents", "distances"]
        )
        user_chunks = process_results(results_user, "user_docs", norm_q)
        
        # If semantic search returned zero results above threshold, fall back to forced sequential retrieval
        if not user_chunks:
            doc_ids_to_use = [d["id"] for d in active_conv_docs if d.get("id")]
            if doc_ids_to_use:
                user_chunks = force_retrieve_user_doc_chunks(
                    session_id,
                    conversation_id=conversation_id,
                    document_ids=doc_ids_to_use,
                    n=8,
                )

    # 4. Consolidated Domain Classification & ChromaDB Retrieval
    domain_label, domain_conf = classify_domain(query)
    effective_domain = query_domain if query_domain in ["Medical", "Banking", "Legal"] else domain_label

    where_clause = None
    if effective_domain == "Medical":
        where_clause = {"domain": {"$in": ["hospital", "medical", "common"]}}
    elif effective_domain == "Banking":
        where_clause = {"domain": "banking"}
    elif effective_domain == "Legal":
        where_clause = {"domain": {"$in": ["legal", "constitution_and_general_law"]}}

    kb_chunks = []
    kb_collection = kb_pipeline.get_chroma_collection()
    
    try:
        query_kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": 30,
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
                n_results=30,
                include=["metadatas", "documents", "distances"]
            )
            kb_chunks = process_results(results_global, "knowledge_base", norm_q)
        except Exception:
            kb_chunks = []

    # Strict domain isolation: purge cross-domain chunks based on effective domain
    if effective_domain == "Medical":
        kb_chunks = [c for c in kb_chunks if "constitution" not in c.get("source", "").lower() and "banking" not in c.get("source", "").lower() and c.get("domain") not in ("banking", "legal", "constitution_and_general_law")]
    elif effective_domain == "Banking":
        kb_chunks = [c for c in kb_chunks if "medical" not in c.get("source", "").lower() and "hospital" not in c.get("source", "").lower() and c.get("domain") not in ("medical", "hospital", "legal")]
    elif effective_domain == "Legal":
        kb_chunks = [c for c in kb_chunks if "banking" not in c.get("source", "").lower() and "medical" not in c.get("source", "").lower() and c.get("domain") not in ("medical", "hospital", "banking")]

    # Language-aware filtering for KB chunks
    if query_language:
        if query_language == "English":
            lang_filtered = [c for c in kb_chunks if "_hi" not in c["source"].lower().split(".")[0][-3:]]
            if lang_filtered:
                kb_chunks = lang_filtered
        elif query_language == "Hindi":
            lang_filtered = [c for c in kb_chunks if "_en" not in c["source"].lower().split(".")[0][-3:]]
            if lang_filtered:
                kb_chunks = lang_filtered

    # Prioritize Curated Local Markdown KB Files (.md) without modifying raw similarity scores
    md_chunks = []
    pdf_chunks = []

    for chunk in kb_chunks:
        src_lower = chunk.get("source", "").lower()
        if src_lower.endswith(".md") or src_lower.endswith(".txt") or "kb_md_" in str(chunk.get("id", "")):
            md_chunks.append(chunk)
        else:
            pdf_chunks.append(chunk)

    md_chunks = sorted(md_chunks, key=lambda x: x["similarity_score"], reverse=True)
    pdf_chunks = sorted(pdf_chunks, key=lambda x: x["similarity_score"], reverse=True)

    # Prioritize Curated Local Markdown KB Files (.md) when relevant match exists
    if md_chunks and md_chunks[0]["similarity_score"] >= 0.25:
        kb_chunks = md_chunks
    else:
        kb_chunks = md_chunks + pdf_chunks



    # Merge, rank, and strictly clamp similarity scores within [0.0, 1.0]
    user_chunks = sorted(user_chunks, key=lambda x: x["similarity_score"], reverse=True)
    kb_chunks = sorted(kb_chunks, key=lambda x: x["similarity_score"], reverse=True)
    
    if len(user_chunks) > 0:
        kb_chunks = []
        
    merged_chunks = user_chunks + kb_chunks

    # Enforce strict score bounding [0.0, 1.0]
    for c in merged_chunks:
        c["similarity_score"] = min(max(float(c.get("similarity_score", 0.0)), 0.0), 1.0)
    
    final_chunks = merged_chunks[:8]
    
    user_docs_used = sum(1 for c in final_chunks if c.get("collection") == "user_docs")
    kb_used = sum(1 for c in final_chunks if c.get("collection") == "knowledge_base")
    
    return {
        "expanded_query": expanded_query,
        "context_chunks": final_chunks,
        "user_doc_chunks_used": user_docs_used,
        "knowledge_base_chunks_used": kb_used,
        "has_any_context": len(final_chunks) > 0,
        "forced_user_doc_retrieval": False
    }

