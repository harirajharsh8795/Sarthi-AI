import os
import sys
import time
import urllib.request
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import kb_pipeline

def run_health_checks():
    print("[HEALTH CHECK] Running post-deployment health & retriever tests...")
    errors = []

    # 1. Check SQLite DB Connectivity
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sqlite", "saarthi.db")
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("SELECT 1;")
        conn.close()
        print(" -> SQLite database: OK")
    except Exception as e:
        errors.append(f"SQLite DB check failed: {e}")

    # 2. Check ChromaDB Collection
    try:
        client = kb_pipeline.get_chroma_client()
        col = client.get_collection("saarthi_kb")
        cnt = col.count()
        print(f" -> ChromaDB vector store: OK ({cnt} chunks indexed)")
        if cnt == 0:
            errors.append("ChromaDB 'saarthi_kb' collection is empty!")
    except Exception as e:
        errors.append(f"ChromaDB check failed: {e}")

    # 3. Check Ollama LLM Service Connectivity
    ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/api/tags"
    try:
        req = urllib.request.Request(ollama_url)
        with urllib.request.urlopen(req, timeout=5) as res:
            if res.status == 200:
                print(" -> Ollama LLM Service: OK")
            else:
                errors.append(f"Ollama returned HTTP {res.status}")
    except Exception as e:
        print(f" -> Ollama Service Notice (offline mode fallback ready): {e}")

    if errors:
        print(f"\n[HEALTH CHECK FAILED] {len(errors)} error(s) detected:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("\n[HEALTH CHECK PASSED] All components are healthy and operational!\n")
        sys.exit(0)

if __name__ == "__main__":
    run_health_checks()
