import os
import uuid
import sqlite3
from datetime import datetime
import session_manager

def init_telemetry_db():
    """Initializes the SQLite tables for tracking LLM inference telemetry."""
    conn = session_manager.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inference_telemetry (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            query_preview TEXT,
            expanded_query_preview TEXT,
            response_language TEXT,
            has_context BOOLEAN,
            skipped_llm BOOLEAN,
            user_doc_chunks_used INTEGER,
            knowledge_base_chunks_used INTEGER,
            total_chunks_in_prompt INTEGER,
            total_tokens_generated INTEGER,
            generation_time_ms INTEGER,
            tokens_per_second REAL,
            model_name TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Add new Stage 2 fields
    new_cols = [
        ("intent", "TEXT"),
        ("detected_domain", "TEXT"),
        ("rewritten_query", "TEXT"),
        ("query_plan", "TEXT"),
        ("confidence_score", "REAL"),
        ("confidence_label", "TEXT"),
        ("grounding_score", "REAL"),
        ("citation_coverage", "REAL"),
        ("self_eval_summary", "TEXT"),
        ("retrieval_mrr", "REAL"),
        ("retrieval_ndcg", "REAL"),
        ("knowledge_graph", "TEXT")
    ]
    for col_name, col_type in new_cols:
        try:
            cursor.execute(f"ALTER TABLE inference_telemetry ADD COLUMN {col_name} {col_type};")
        except sqlite3.OperationalError:
            pass  # Already exists
            
    conn.commit()
    conn.close()

def log_inference(
    session_id, query, expanded_query, response_language, has_context, skipped_llm,
    user_doc_chunks_used, knowledge_base_chunks_used, total_chunks_in_prompt,
    total_tokens_generated, generation_time_ms, tokens_per_second, model_name="llama3.2:1b",
    intent=None, detected_domain=None, rewritten_query=None, query_plan=None,
    confidence_score=None, confidence_label=None, grounding_score=None,
    citation_coverage=None, self_eval_summary=None, retrieval_mrr=None,
    retrieval_ndcg=None, knowledge_graph=None
):
    """
    Logs an inference event with full Stage 2 telemetry metrics to SQLite.
    """
    init_telemetry_db()
    conn = session_manager.get_db_connection()
    cursor = conn.cursor()
    
    inference_id = str(uuid.uuid4())
    query_preview = (query[:80] + "...") if query and len(query) > 80 else (query or "")
    expanded_query_preview = (expanded_query[:80] + "...") if expanded_query and len(expanded_query) > 80 else (expanded_query or "")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query_plan_str = json.dumps(query_plan) if isinstance(query_plan, (list, dict)) else query_plan
    knowledge_graph_str = json.dumps(knowledge_graph) if isinstance(knowledge_graph, (list, dict)) else knowledge_graph

    cursor.execute("""
        INSERT INTO inference_telemetry (
            id, session_id, query_preview, expanded_query_preview, response_language,
            has_context, skipped_llm, user_doc_chunks_used, knowledge_base_chunks_used,
            total_chunks_in_prompt, total_tokens_generated, generation_time_ms,
            tokens_per_second, model_name, timestamp, intent, detected_domain,
            rewritten_query, query_plan, confidence_score, confidence_label,
            grounding_score, citation_coverage, self_eval_summary, retrieval_mrr,
            retrieval_ndcg, knowledge_graph
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        inference_id, session_id, query_preview, expanded_query_preview, response_language,
        int(has_context), int(skipped_llm), user_doc_chunks_used, knowledge_base_chunks_used,
        total_chunks_in_prompt, total_tokens_generated, generation_time_ms,
        tokens_per_second, model_name, now_str, intent, detected_domain,
        rewritten_query, query_plan_str, confidence_score, confidence_label,
        grounding_score, citation_coverage, self_eval_summary, retrieval_mrr,
        retrieval_ndcg, knowledge_graph_str
    ))
    conn.commit()
    conn.close()
    return inference_id

def get_recent_telemetry(n=20):
    """Retrieves up to n recent telemetry records, ordered from newest to oldest."""
    conn = session_manager.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM inference_telemetry
        ORDER BY timestamp DESC
        LIMIT ?
    """, (n,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_telemetry_by_id(inference_id: str):
    """Fetches a specific telemetry record by its ID."""
    conn = session_manager.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inference_telemetry WHERE id = ?", (inference_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

