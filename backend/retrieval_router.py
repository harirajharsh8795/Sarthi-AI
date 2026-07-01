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
    Computes exact Cosine Similarity from squared L2 distance and vector norms.
    """
    chunks = []
    if not query_results or not query_results.get('ids') or len(query_results['ids'][0]) == 0:
        return chunks
        
    ids = query_results['ids'][0]
    distances = query_results['distances'][0]
    metadatas = query_results['metadatas'][0]
    documents = query_results['documents'][0]
    embeddings = query_results.get('embeddings')
    
    # Grab first list element if embeddings is returned as nested list
    db_embs = embeddings[0] if embeddings else None
    
    for i in range(len(ids)):
        dist = distances[i]
        
        # Exact Cosine Similarity formula using norms and squared L2 distance:
        # L2_dist = ||q||^2 + ||db||^2 - 2 * ||q|| * ||db|| * cos_sim
        # => cos_sim = (||q||^2 + ||db||^2 - L2_dist) / (2 * ||q|| * ||db||)
        if db_embs is not None and len(db_embs) > i and db_embs[i] is not None:
            emb_db = np.array(db_embs[i])
            norm_db = np.linalg.norm(emb_db)
            if norm_q > 0 and norm_db > 0:
                sim = (norm_q**2 + norm_db**2 - dist) / (2.0 * norm_q * norm_db)
            else:
                sim = 0.0
        else:
            # Safe linear fallback if embeddings are missing
            sim = 1.0 - (dist / 20.0)
            
        required_threshold = USER_DOC_MIN_SIMILARITY if collection_name == "user_docs" else MIN_SIMILARITY_SCORE
        if sim >= required_threshold:
            meta = metadatas[i]
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
    Detects trigger phrases indicating the user wants to ask about their uploaded document.
    """
    if not query:
        return False
    query_lower = query.lower()
    trigger_phrases = [
        "pdf", "document", "uploaded file", "is file", "jo upload",
        "summary do", "samjhao", "explain karo", "kya hai is",
        "explain this", "summarize", "summarise", "about this file",
        "mera document", "maine upload kiya"
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

def retrieve_context(query: str, session_id: str | None, conversation_id: str | None = None) -> dict:
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

    # 1. Expand query via Stage 0 Glossary
    expanded_query = expand_query_with_glossary(query)
    
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
            include=["metadatas", "documents", "distances", "embeddings"]
        )
        user_chunks = process_results(results_user, "user_docs", norm_q)
        
        # User Doc Topic Filter (Fix 1 Addendum):
        # If this is not an explicit document summary query, exclude weak user document chunks (similarity < 0.50)
        # to prevent unrelated uploads from appearing in general queries.
        if not is_document_about_query(query):
            user_chunks = [c for c in user_chunks if c["similarity_score"] >= 0.50]
        
    # 4. Retrieve from knowledge_base for each domain to ensure high recall across domains
    domains = ["banking", "legal", "constitution_and_general_law", "hospital"]
    kb_chunks = []
    kb_collection = kb_pipeline.get_chroma_collection()
    
    for dom in domains:
        try:
            results_dom = kb_collection.query(
                query_embeddings=[query_embedding],
                n_results=10,
                where={"domain": dom},
                include=["metadatas", "documents", "distances", "embeddings"]
            )
            chunks_dom = process_results(results_dom, "knowledge_base", norm_q)
            kb_chunks.extend(chunks_dom)
        except Exception as query_err:
            # Fallback in case a domain filter query errors out
            pass

    # 4.5 Apply keyword/filename boosts to kb_chunks to improve precision and rank relevant documents first
    query_lower = query.lower()
    
    # RTI Boost
    if any(k in query_lower for k in ["rti", "right to information", "सूचना का अधिकार", "suchna ka adhikar"]):
        for chunk in kb_chunks:
            if "rti" in chunk["source"].lower():
                chunk["similarity_score"] += 0.25
                
    # KYC Boost
    if "kyc" in query_lower:
        for chunk in kb_chunks:
            if "kyc" in chunk["source"].lower():
                chunk["similarity_score"] += 0.25
                
    # Consumer Protection Boost
    if any(k in query_lower for k in ["consumer", "upbhokta", "उपभोक्ता", "shikayat", "complaint"]):
        for chunk in kb_chunks:
            if "consumer" in chunk["source"].lower():
                chunk["similarity_score"] += 0.25

    # 5. Merge and rank
    # Sort each set descending by similarity score
    user_chunks = sorted(user_chunks, key=lambda x: x["similarity_score"], reverse=True)
    kb_chunks = sorted(kb_chunks, key=lambda x: x["similarity_score"], reverse=True)
    
    # Tiered ranking: user_docs has absolute priority
    merged_chunks = user_chunks + kb_chunks
    
    # Cap total context chunks to 10
    final_chunks = merged_chunks[:10]
    
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
