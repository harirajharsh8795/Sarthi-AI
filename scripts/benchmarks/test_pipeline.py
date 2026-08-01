import os
import sys
import json
import sqlite3

# Ensure current directory is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import kb_pipeline
from glossary.query_expander import expand_query_with_glossary

def run_tests():
    print("=== Saarthi AI Seeding Pipeline Verification Tests ===")
    errors = 0
    
    # 1. Directory Structure Test
    print("\n[Test 1] Folder Structure Verification:")
    expected_dirs = [
        "./data/knowledge_base",
        "./data/chroma_db",
        "./data/sqlite",
        "./glossary"
    ]
    for d in expected_dirs:
        if os.path.exists(d):
            print(f"  [OK] Directory '{d}' exists.")
        else:
            print(f"  [FAIL] Directory '{d}' is missing.")
            errors += 1
            
    # 2. SQLite Database Verification
    print("\n[Test 2] SQLite Database Verification:")
    if os.path.exists(kb_pipeline.DB_PATH):
        print(f"  [OK] Database file '{kb_pipeline.DB_PATH}' exists.")
        try:
            conn = kb_pipeline.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kb_documents'")
            table_exists = cursor.fetchone()
            if table_exists:
                print("  [OK] Table 'kb_documents' exists.")
                cursor.execute("SELECT count(*) as cnt FROM kb_documents")
                cnt = cursor.fetchone()['cnt']
                print(f"  [OK] 'kb_documents' contains {cnt} entries.")
            else:
                print("  [FAIL] Table 'kb_documents' does not exist.")
                errors += 1
            conn.close()
        except Exception as e:
            print(f"  [FAIL] Error querying SQLite: {e}")
            errors += 1
    else:
        print(f"  [FAIL] SQLite database file is missing at {kb_pipeline.DB_PATH}")
        errors += 1
        
    # 3. ChromaDB Verification
    print("\n[Test 3] ChromaDB Collection Verification:")
    if os.path.exists(kb_pipeline.CHROMA_DIR):
        print(f"  [OK] ChromaDB directory '{kb_pipeline.CHROMA_DIR}' exists.")
        try:
            collection = kb_pipeline.get_chroma_collection()
            count = collection.count()
            print(f"  [OK] ChromaDB 'knowledge_base' collection is accessible.")
            print(f"  [OK] Collection contains {count} chunks.")
            if count > 0:
                # Test retrieving a sample record
                peek = collection.peek(limit=1)
                if peek and peek['ids']:
                    print(f"  [OK] Sample chunk ID retrieved: {peek['ids'][0]}")
                    print(f"  [OK] Sample chunk metadata: {peek['metadatas'][0]}")
                else:
                    print("  [FAIL] Collection is empty but count is positive?")
                    errors += 1
        except Exception as e:
            print(f"  [FAIL] Error accessing ChromaDB: {e}")
            errors += 1
    else:
        print("  [FAIL] ChromaDB folder is missing.")
        errors += 1
        
    # 4. Hinglish Medical Glossary and Query Expander Verification
    print("\n[Test 4] Query Expansion Verification:")
    test_queries = [
        ("Mujhe bukhar aur sir dard hai", ["fever", "headache"]),
        ("उसका पेट दर्द और उल्टी ठीक नहीं हो रहा", ["abdominal pain", "vomiting"]),
        ("mere gale me kharas hai aur saans phulna shuru ho gaya", ["sore throat", "breathlessness"]),
        ("BP ki problem and sugar", ["hypertension", "diabetes"])
    ]
    
    for q, expected_keywords in test_queries:
        expanded = expand_query_with_glossary(q)
        # Encode print safely for Windows CP1252 console
        safe_q = q.encode('ascii', 'replace').decode('ascii')
        safe_expanded = expanded.encode('ascii', 'replace').decode('ascii')
        print(f"  Query:    '{safe_q}'")
        print(f"  Expanded: '{safe_expanded}'")
        
        all_found = True
        for kw in expected_keywords:
            if kw.lower() not in expanded.lower():
                print(f"    [FAIL] Missing expected translation keyword: '{kw}'")
                all_found = False
                
        if all_found:
            print("    [OK] Query expansion match successful.")
        else:
            errors += 1
            
    print("\n==========================================")
    if errors == 0:
        print("ALL TESTS PASSED SUCCESSFULLY!")
    else:
        print(f"TEST RUN COMPLETED WITH {errors} FAILURE(S).")
    print("==========================================")
    return errors == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
