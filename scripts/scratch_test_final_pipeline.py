import requests
import json
import base64
import time
import os

base_url = "http://localhost:8000"

def test_final_pipeline():
    print("=== FINAL PIPELINE TESTS ===")
    
    # 1. Create a session & conversation
    session_id = "test_final_session"
    requests.post(f"{base_url}/api/session", json={"session_id": session_id, "display_name": "Final Tester"})
    
    r_conv = requests.post(f"{base_url}/api/conversations", json={"session_id": session_id, "title": "New Conversation"})
    conv_id = r_conv.json()["conversation_id"]
    print(f"[1] Created conversation: {conv_id}")
    
    # 2. Upload PNG (OCR test)
    png_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
    files = {"file": ("test.png", png_data, "image/png")}
    data = {"session_id": session_id, "conversation_id": conv_id}
    r_upload = requests.post(f"{base_url}/api/upload", files=files, data=data)
    print(f"[2] Upload PNG status: {r_upload.status_code}")
    doc_id = r_upload.json()["document_id"]
    
    # Wait for ingestion to complete
    print("[3] Waiting 15s for background ingestion (OCR -> Embedding -> Indexing)...")
    time.sleep(15)
    
    # 4. Check if document is READY in history
    r_hist = requests.get(f"{base_url}/api/history?session_id={session_id}&conversation_id={conv_id}")
    history = r_hist.json()
    docs = history.get("documents", [])
    print(f"[4] History fetched. Found {len(docs)} documents.")
    for d in docs:
        print(f"    - {d['original_filename']}: status={d.get('status')}")
    
    # 5. Query LLM to ensure retrieval works
    print("[5] Querying LLM...")
    r_query = requests.get(f"{base_url}/api/stream?query=What%20is%20this%3F&session_id={session_id}&conversation_id={conv_id}")
    print(f"    Stream status: {r_query.status_code}")
    
    # 6. Delete document
    print("[6] Deleting document...")
    r_del_doc = requests.delete(f"{base_url}/api/document/{doc_id}?session_id={session_id}")
    print(f"    Delete doc status: {r_del_doc.status_code}")
    
    # 7. Delete conversation
    print("[7] Deleting conversation...")
    r_del_conv = requests.delete(f"{base_url}/api/conversations/{conv_id}?session_id={session_id}")
    print(f"    Delete conv status: {r_del_conv.status_code}")

if __name__ == "__main__":
    test_final_pipeline()
