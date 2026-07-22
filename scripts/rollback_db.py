import os
import sys
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
BACKUP_DIR = os.path.join(ROOT_DIR, "backups")
LATEST_MARKER = os.path.join(BACKUP_DIR, "LATEST_BACKUP")

def rollback_to_latest_backup():
    print("[ROLLBACK] Initiating automated database & index rollback...")
    if not os.path.exists(LATEST_MARKER):
        print("[ROLLBACK ERROR] No previous backup marker found! Rollback aborted.")
        sys.exit(1)
        
    with open(LATEST_MARKER, "r") as f:
        backup_folder = f.read().strip()

    if not os.path.exists(backup_folder):
        print(f"[ROLLBACK ERROR] Backup folder {backup_folder} does not exist!")
        sys.exit(1)

    print(f"[ROLLBACK] Restoring from: {backup_folder}")

    # 1. Restore SQLite
    sq_backup = os.path.join(backup_folder, "saarthi.db")
    sq_target = os.path.join(DATA_DIR, "sqlite", "saarthi.db")
    if os.path.exists(sq_backup):
        os.makedirs(os.path.dirname(sq_target), exist_ok=True)
        shutil.copy2(sq_backup, sq_target)
        print(" -> SQLite database restored.")

    # 2. Restore ChromaDB
    ch_backup = os.path.join(backup_folder, "chroma_db")
    ch_target = os.path.join(DATA_DIR, "chroma_db")
    if os.path.exists(ch_backup):
        if os.path.exists(ch_target):
            shutil.rmtree(ch_target)
        shutil.copytree(ch_backup, ch_target)
        print(" -> ChromaDB vector store restored.")

    # 3. Restore BM25 Index
    bm_backup = os.path.join(backup_folder, "bm25_index.pkl")
    bm_target = os.path.join(DATA_DIR, "bm25_index.pkl")
    if os.path.exists(bm_backup):
        shutil.copy2(bm_backup, bm_target)
        print(" -> BM25 index restored.")

    # 4. Restore Knowledge Graph
    kg_backup = os.path.join(backup_folder, "knowledge_graph.json")
    kg_target = os.path.join(DATA_DIR, "knowledge_graph.json")
    if os.path.exists(kg_backup):
        shutil.copy2(kg_backup, kg_target)
        print(" -> Knowledge Graph restored.")

    print("[ROLLBACK SUCCESS] Database and RAG indexes restored cleanly to pre-deployment state.\n")

if __name__ == "__main__":
    rollback_to_latest_backup()
