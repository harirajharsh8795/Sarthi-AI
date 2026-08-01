import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
import kb_pipeline
import retrieval_router

session_id = "test_doc_debug_sess"
conv_id = "test_doc_debug_conv"
img_path = r"C:\Users\HP\.gemini\antigravity-ide\brain\f75faf6d-afdc-47e5-94dd-6e2ace58324c\media__1785519886716.png"

from job_queue import job_queue
doc_id = f"doc_{int(time.time())}"
job_id = job_queue.create_job(doc_id, "upload")
kb_pipeline.ingest_user_document_task(job_id, img_path, "holy_family.webp", session_id, conversation_id=conv_id, document_id=doc_id)

# Retrieve
res = retrieval_router.retrieve_context("is report me patient ka naam aur age kya hai?", session_id, conv_id)

chunks = res.get("context_chunks", [])
print(f"DEBUG: Retrieved {len(chunks)} chunks!")
for c in chunks:
    print(f"Collection: {c.get('collection')} | Text snippet: {c.get('text')[:150]}")
