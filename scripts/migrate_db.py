import os
import sqlite3

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "data", "sqlite", "saarthi.db")

def run_migrations():
    print(f"[MIGRATION] Checking & applying database schema migrations on {DB_PATH}...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Documents Metadata Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        doc_id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        domain TEXT,
        category TEXT,
        topic TEXT,
        language TEXT,
        content_hash TEXT,
        chunks_count INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 2. Query Logs & Telemetry Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS query_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        domain_hint TEXT,
        chunks_retrieved INTEGER,
        latency_ms REAL,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 3. System Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpu_usage REAL,
        ram_usage REAL,
        gpu_usage REAL,
        ollama_status TEXT,
        chroma_status TEXT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print("[MIGRATION SUCCESS] All database tables & indices are up to date.\n")

if __name__ == "__main__":
    run_migrations()
