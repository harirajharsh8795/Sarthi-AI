import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
import llm_inference
import session_manager
import kb_pipeline

session_id = f"sess_full_text_{int(time.time())}"
conversation_id = f"conv_full_text_{int(time.time())}"
session_manager.get_or_create_session(session_id, "Full Answer Exporter")

# Index Holy Family Hospital Medical Report
img_path = r"C:\Users\HP\.gemini\antigravity-ide\brain\f75faf6d-afdc-47e5-94dd-6e2ace58324c\media__1785519886716.png"
if os.path.exists(img_path):
    doc_id = f"doc_{int(time.time())}"
    session_manager.create_document_record(doc_id, session_id, "medical_report.webp", "webp", conversation_id=conversation_id)
    kb_pipeline.process_user_document_sync(img_path, session_id, conversation_id, "medical_report.webp", doc_id)

TEST_QUERIES = [
    {"q": "pet dard ki dva btao", "lang": "Hinglish", "cat": "Medical"},
    {"q": "bukhar me kya karna chahiye?", "lang": "Hinglish", "cat": "Medical"},
    {"q": "How to update KYC in bank account?", "lang": "English", "cat": "Banking"},
    {"q": "RTI application kaise file karein aur kitne din me jawab milta hai?", "lang": "Hinglish", "cat": "Legal"},
    {"q": "report ko summarize kro", "lang": "Hinglish", "cat": "Document Analysis"},
    {"q": "is report me patient ka naam aur age kya hai?", "lang": "Hinglish", "cat": "Document Analysis"},
    {"q": "HBsAG test ka result kya aaya hai report me?", "lang": "Hinglish", "cat": "Document Analysis"}
]

out = []

for item in TEST_QUERIES:
    q = item["q"]
    lang = item["lang"]
    cat = item["cat"]
    
    tokens = []
    for event in llm_inference.generate_answer_stream(q, session_id, lang, conversation_id):
        if event.get("type") == "token":
            t = event.get("data", {}).get("token", "")
            if t:
                tokens.append(t)
                
    full_answer = "".join(tokens).strip()
    out.append({"query": q, "category": cat, "language": lang, "answer": full_answer})

out_file = os.path.join(os.path.dirname(__file__), "sample_full_answers.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"Generated {len(out)} full answers in {out_file}")
