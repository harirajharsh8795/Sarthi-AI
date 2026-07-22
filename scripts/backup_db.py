import os
import sys
import time
import shutil
import tarfile

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
BACKUP_DIR = os.path.join(ROOT_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

def create_pre_deployment_backup():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(BACKUP_DIR, f"backup_{timestamp}")
    os.makedirs(backup_folder, exist_ok=True)
    
    print(f"[BACKUP] Creating pre-deployment backup at: {backup_folder}")
    
    # 1. SQLite Database Backup
    sqlite_db = os.path.join(DATA_DIR, "sqlite", "saarthi.db")
    if os.path.exists(sqlite_db):
        shutil.copy2(sqlite_db, os.path.join(backup_folder, "saarthi.db"))
        print(" -> SQLite database backed up.")

    # 2. ChromaDB Backup
    chroma_dir = os.path.join(DATA_DIR, "chroma_db")
    if os.path.exists(chroma_dir):
        shutil.copytree(chroma_dir, os.path.join(backup_folder, "chroma_db"))
        print(" -> ChromaDB vector store backed up.")

    # 3. BM25 Index Backup
    bm25_file = os.path.join(DATA_DIR, "bm25_index.pkl")
    if os.path.exists(bm25_file):
        shutil.copy2(bm25_file, os.path.join(backup_folder, "bm25_index.pkl"))
        print(" -> BM25 index backed up.")

    # 4. Knowledge Graph Backup
    kg_file = os.path.join(DATA_DIR, "knowledge_graph.json")
    if os.path.exists(kg_file):
        shutil.copy2(kg_file, os.path.join(backup_folder, "knowledge_graph.json"))
        print(" -> Knowledge Graph backed up.")

    # Record latest backup marker file
    latest_marker = os.path.join(BACKUP_DIR, "LATEST_BACKUP")
    with open(latest_marker, "w") as f:
        f.write(backup_folder)
        
    print(f"[BACKUP SUCCESS] Backup complete: {backup_folder}\n")
    return backup_folder

if __name__ == "__main__":
    create_pre_deployment_backup()
