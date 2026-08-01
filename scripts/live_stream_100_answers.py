import os
import sys
import time
import json
import logging

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import llm_inference
import session_manager

logging.basicConfig(level=logging.WARNING)

# 100 Diverse Questions List
QUESTIONS = [
    # ── Medical
    {"q": "pet dard ki dva btao", "lang": "Hinglish"},
    {"q": "bukhar me kya karna chahiye?", "lang": "Hinglish"},
    {"q": "मुझे तेज बुखार और सिरदर्द है, क्या प्राथमिक उपचार करूं?", "lang": "Hindi"},
    {"q": "What are the early symptoms of Dengue fever?", "lang": "English"},
    {"q": "khansi aur gale me kharash ki home remedy btao", "lang": "Hinglish"},
    {"q": "blood pressure high hone par kya dawai lein?", "lang": "Hinglish"},
    {"q": "मधुमेह (Diabetes) के मुख्य लक्षण क्या होते हैं?", "lang": "Hindi"},
    {"q": "What is the recommended first aid for minor skin burns?", "lang": "English"},
    {"q": "vomiting aur loose motion rokne ke liye kya karein", "lang": "Hinglish"},
    {"q": "acidity aur chest pain me kya antar hai?", "lang": "Hinglish"},
    
    # ── Banking
    {"q": "How to update KYC in bank account?", "lang": "English"},
    {"q": "bank account me kyc update karne ke liye konse documents zaroori hain?", "lang": "Hinglish"},
    {"q": "बैंक खाते में केवाईसी (KYC) कराने की क्या प्रक्रिया है?", "lang": "Hindi"},
    {"q": "What is the procedure for reporting unauthorized ATM transaction?", "lang": "English"},
    {"q": "unauthorized transaction hone par rbi rules ke according kitne ghante me complaint karein?", "lang": "Hinglish"},
    {"q": "atm card kho jane par block kaise karein?", "lang": "Hinglish"},
    
    # ── Legal
    {"q": "What is the procedure to file an RTI application?", "lang": "English"},
    {"q": "RTI application kaise file karein aur kitne din me jawab milta hai?", "lang": "Hinglish"},
    {"q": "सूचना का अधिकार (RTI) आवेदन पत्र कैसे लिखें?", "lang": "Hindi"},
    {"q": "police station me FIR darj na karne par kya karein?", "lang": "Hinglish"},
    {"q": "What are the consumer rights under Consumer Protection Act 2019?", "lang": "English"},

    # ── Document Summarization
    {"q": "report ko summarize kro", "lang": "Hinglish"},
    {"q": "reeport ko smjhao ache se", "lang": "Hinglish"},
    {"q": "is report me patient ka naam aur age kya hai?", "lang": "Hinglish"},
    {"q": "HBsAG test ka result kya aaya hai report me?", "lang": "Hinglish"},
]

def run_live_stream_terminal():
    session_id = f"term_stream_{int(time.time())}"
    conversation_id = f"conv_term_{int(time.time())}"
    session_manager.get_or_create_session(session_id, "Terminal Live Stream")

    # Index BOTH uploaded medical report images for complete document benchmark testing
    import kb_pipeline
    reports = [
        (r"C:\Users\HP\.gemini\antigravity-ide\brain\f75faf6d-afdc-47e5-94dd-6e2ace58324c\media__1785519886716.png", "holy_family_medical_report.webp"),
        (r"C:\Users\HP\.gemini\antigravity-ide\brain\f75faf6d-afdc-47e5-94dd-6e2ace58324c\media__1785519478171.png", "lft_liver_report.webp")
    ]
    for idx, (fpath, fname) in enumerate(reports, 1):
        if os.path.exists(fpath):
            print(f"📄 Indexing report [{idx}/2] '{fname}' into ChromaDB user_docs...")
            try:
                doc_id = f"doc_{idx}_{int(time.time())}"
                session_manager.save_user_document(doc_id, session_id, conversation_id, fname, "webp", status="pending")
                kb_pipeline.process_user_document(fpath, session_id, conversation_id, fname, doc_id)
                print(f"✅ Report '{fname}' indexed successfully!")
            except Exception as e:
                print(f"⚠️ Indexing warning for '{fname}': {e}")

    print("\n" + "="*80)
    print("🚀 SAARTHI AI: INSTANT LIVE TERMINAL STREAMING ANSWERS TEST")
    print("="*80 + "\n")

    for i, item in enumerate(QUESTIONS, 1):
        query = item["q"]
        lang = item["lang"]

        print(f"\n{"─"*80}")
        print(f"❓ QUESTION [{i}/{len(QUESTIONS)}] ({lang}): {query}")
        print(f"{"─"*80}")
        print("💡 SAARTHI AI ANSWER:\n")

        sys.stdout.flush()

        start_time = time.perf_counter()
        first_token_time = None
        total_tokens = 0

        # Stream response token-by-token live to terminal
        for event in llm_inference.generate_answer_stream(query, session_id, lang, conversation_id):
            if event.get("type") == "token":
                token = event.get("data", {}).get("token", "")
                if token:
                    if first_token_time is None:
                        first_token_time = time.perf_counter() - start_time
                    sys.stdout.write(token)
                    sys.stdout.flush()
                    total_tokens += 1

        total_time = time.perf_counter() - start_time
        ttft_ms = round(first_token_time * 1000, 1) if first_token_time else 0.0
        
        print("\n\n" + "·"*80)
        print(f"⏱️ Time-To-First-Token (TTFT): {ttft_ms} ms | Total Generation Time: {round(total_time, 2)}s | Tokens: {total_tokens}")
        print("·"*80 + "\n")
        
        time.sleep(0.5)

if __name__ == "__main__":
    run_live_stream_terminal()
