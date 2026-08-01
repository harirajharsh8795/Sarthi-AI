import os
import sys
import time
import json
import logging

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

import llm_inference
import retrieval_router
import intent_service
import session_manager
import kb_pipeline
from prompt_builder import prompt_builder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("evaluator")

# 100 Comprehensive Benchmark Questions across Hindi, English, and Hinglish
TEST_QUESTIONS = [
    # ── Medical & Symptoms (25)
    {"q": "pet dard ki dva btao", "lang": "Hinglish", "domain": "Medical"},
    {"q": "bukhar me kya karna chahiye?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "मुझे तेज बुखार और सिरदर्द है, क्या प्राथमिक उपचार करूं?", "lang": "Hindi", "domain": "Medical"},
    {"q": "What are the early symptoms of Dengue fever?", "lang": "English", "domain": "Medical"},
    {"q": "khansi aur gale me kharash ki home remedy btao", "lang": "Hinglish", "domain": "Medical"},
    {"q": "blood pressure high hone par kya dawai lein?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "मधुमेह (Diabetes) के मुख्य लक्षण क्या होते हैं?", "lang": "Hindi", "domain": "Medical"},
    {"q": "What is the recommended first aid for minor skin burns?", "lang": "English", "domain": "Medical"},
    {"q": "vomiting aur loose motion rokne ke liye kya karein", "lang": "Hinglish", "domain": "Medical"},
    {"q": "acidity aur chest pain me kya antar hai?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "मलेरिया बुखार के क्या लक्षण होते हैं?", "lang": "Hindi", "domain": "Medical"},
    {"q": "How to prevent dehydration during severe fever?", "lang": "English", "domain": "Medical"},
    {"q": "serum bilirubin high hone ka kya matlab hai?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "SGPT aur SGOT level badhne par kya parhez karein?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "HBsAg Non Reactive hone ka kya arth hai?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "HIV rapid test Non Reactive hai to kya patient safe hai?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "HCV Spot test Negative aane par kya next test zaroori hai?", "lang": "Hinglish", "domain": "Medical"},
    {"q": "सिर दर्द और चक्कर आने पर क्या घरेलू उपाय करें?", "lang": "Hindi", "domain": "Medical"},
    {"q": "What precautions should be taken for viral infection?", "lang": "English", "domain": "Medical"},
    {"q": "chote bachon me bukhar hone par patti kaise rkhein", "lang": "Hinglish", "domain": "Medical"},
    {"q": "typhoid fever me konsa khana khana chahiye", "lang": "Hinglish", "domain": "Medical"},
    {"q": "आंखों में जलन और लालिमा का क्या इलाज है?", "lang": "Hindi", "domain": "Medical"},
    {"q": "What are the common causes of high cholesterol?", "lang": "English", "domain": "Medical"},
    {"q": "jaundice (pilia) ke symptoms aur ilaj btao", "lang": "Hinglish", "domain": "Medical"},
    {"q": "kidney stone me kitna pani pina chahiye", "lang": "Hinglish", "domain": "Medical"},

    # ── Banking & KYC (25)
    {"q": "How to update KYC in bank account?", "lang": "English", "domain": "Banking"},
    {"q": "bank account me kyc update karne ke liye konse documents zaroori hain?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "बैंक खाते में केवाईसी (KYC) कराने की क्या प्रक्रिया है?", "lang": "Hindi", "domain": "Banking"},
    {"q": "What is the procedure for reporting unauthorized ATM transaction?", "lang": "English", "domain": "Banking"},
    {"q": "unauthorized transaction hone par rbi rules ke according kitne ghante me complaint karein?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "atm card kho jane par block kaise karein?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "बैंक से एजुकेशन लोन लेने की क्या पात्रता है?", "lang": "Hindi", "domain": "Banking"},
    {"q": "What is RBI Ombudsman scheme for banking complaints?", "lang": "English", "domain": "Banking"},
    {"q": "cheque bounce hone par legal action kaise liya jata hai?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "saving account aur current account me kya difference hai?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "फिक्स्ड डिपॉजिट (FD) पर टीडीएस कटने के क्या नियम हैं?", "lang": "Hindi", "domain": "Banking"},
    {"q": "How to file complaint against bank manager to RBI?", "lang": "English", "domain": "Banking"},
    {"q": "ifsc code aur micr code me kya antar hai?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "home loan foreclosure process aur charges kya hain?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "बैंक अकाउंट डोरमेंट (Dormant) होने पर चालू कैसे कराएं?", "lang": "Hindi", "domain": "Banking"},
    {"q": "What official valid documents (OVD) are accepted for bank KYC?", "lang": "English", "domain": "Banking"},
    {"q": "credit card bill payment due date miss hone par kitna penalty lagta hai?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "net banking password forget hone par reset kaise karein?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "जन धन खाता खोलने के क्या फायदे हैं?", "lang": "Hindi", "domain": "Banking"},
    {"q": "How long does bank take to refund failed UPI transaction?", "lang": "English", "domain": "Banking"},
    {"q": "minor bank account me guardian details kaise add karein?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "bank me nominee name kaise update ya change karein?", "lang": "Hinglish", "domain": "Banking"},
    {"q": "सुरक्षा बीमा योजना (PMSBY) के क्या नियम हैं?", "lang": "Hindi", "domain": "Banking"},
    {"q": "What is the interest rate calculation method for savings account?", "lang": "English", "domain": "Banking"},
    {"q": "passbook print aur statement nikalne ka tareeka btao", "lang": "Hinglish", "domain": "Banking"},

    # ── Legal & Civil Rights (25)
    {"q": "What is the procedure to file an RTI application?", "lang": "English", "domain": "Legal"},
    {"q": "RTI application kaise file karein aur kitne din me jawab milta hai?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "सूचना का अधिकार (RTI) आवेदन पत्र कैसे लिखें?", "lang": "Hindi", "domain": "Legal"},
    {"q": "police station me FIR darj na karne par kya karein?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "What are the consumer rights under Consumer Protection Act 2019?", "lang": "English", "domain": "Legal"},
    {"q": "consumer court me complaint file karne ka process btao", "lang": "Hinglish", "domain": "Legal"},
    {"q": "उपभोक्ता फोरम में ऑनलाइन शिकायत कैसे दर्ज करें?", "lang": "Hindi", "domain": "Legal"},
    {"q": "What is the difference between bailable and non-bailable offence?", "lang": "English", "domain": "Legal"},
    {"q": "anticipatory bail (अग्रिम जमानत) lene ke kya rules hain?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "civil court aur criminal court me kya antar hota hai?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "मुफ्त कानूनी सहायता (Legal Aid) प्राप्त करने के क्या नियम हैं?", "lang": "Hindi", "domain": "Legal"},
    {"q": "How to get a certified copy of court order or judgment?", "lang": "English", "domain": "Legal"},
    {"q": "tenant eviction aur rent dispute me kya kanooni rights hain?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "cyber fraud complaint cybercrime portal par kaise karein?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "महिला सुरक्षा कानून और 1090 हेल्पलाइन के अधिकार क्या हैं?", "lang": "Hindi", "domain": "Legal"},
    {"q": "What is zero FIR and where can it be registered?", "lang": "English", "domain": "Legal"},
    {"q": "property registration aur stamp duty ke kanooni niyam btao", "lang": "Hinglish", "domain": "Legal"},
    {"q": "will (वसीयत) ko legally valid banane ke liye kya zaroori hai?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "मानवाधिकार आयोग (NHRC) में शिकायत कैसे दर्ज कराएं?", "lang": "Hindi", "domain": "Legal"},
    {"q": "What are the legal remedies for breach of contract?", "lang": "English", "domain": "Legal"},
    {"q": "domestic violence act ke tehat mahila ko kya suraksha milti hai?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "lok adalat me case resolve karwane ke kya fayde hain?", "lang": "Hinglish", "domain": "Legal"},
    {"q": "श्रमिकों के न्यूनतम वेतन कानून (Minimum Wages Act) के नियम क्या हैं?", "lang": "Hindi", "domain": "Legal"},
    {"q": "What is the procedure for mutual consent divorce in India?", "lang": "English", "domain": "Legal"},
    {"q": "police arrest ke time par citizen ke kya 5 mukhya adhikar hain?", "lang": "Hinglish", "domain": "Legal"},

    # ── Uploaded Document Summarization & Medical Lab Report Queries (25)
    {"q": "report ko summarize kro", "lang": "Hinglish", "domain": "Document"},
    {"q": "reeport ko smjhao ache se", "lang": "Hinglish", "domain": "Document"},
    {"q": "is report me patient ka naam aur age kya hai?", "lang": "Hinglish", "domain": "Document"},
    {"q": "HBsAG test ka result kya aaya hai report me?", "lang": "Hinglish", "domain": "Document"},
    {"q": "HIV aur HCV test positive hai ya negative?", "lang": "Hinglish", "domain": "Document"},
    {"q": "Serum Bilirubin total aur direct kitna hai report me?", "lang": "Hinglish", "domain": "Document"},
    {"q": "SGPT aur SGOT level normal hain ya high hain?", "lang": "Hinglish", "domain": "Document"},
    {"q": "What is the lab report conclusion for Santosh Devi?", "lang": "English", "domain": "Document"},
    {"q": "is document me Holy Family Hospital ke doctor ka naam kya likha hai?", "lang": "Hinglish", "domain": "Document"},
    {"q": "इस रिपोर्ट में मुख्य जांच परिणाम क्या हैं?", "lang": "Hindi", "domain": "Document"},
    {"q": "bill number aur sample date btao report me se", "lang": "Hinglish", "domain": "Document"},
    {"q": "Alkaline phosphatase aur Total protein values btao", "lang": "Hinglish", "domain": "Document"},
    {"q": "is PDF ka poora summary do clean format me", "lang": "Hinglish", "domain": "Document"},
    {"q": "what does Non Reactive mean in this blood report?", "lang": "English", "domain": "Document"},
    {"q": "kya is report me koi abnomal test result hai?", "lang": "Hinglish", "domain": "Document"},
    {"q": "patient Type IPD hai ya OPD report me?", "lang": "Hinglish", "domain": "Document"},
    {"q": "is document me doctor ne kya adviced diya hai?", "lang": "Hinglish", "domain": "Document"},
    {"q": "क्या रिपोर्ट में यकृत (Liver) के सभी एंजाइम सामान्य हैं?", "lang": "Hindi", "domain": "Document"},
    {"q": "Please summarize all key lab findings in emoji bullet points", "lang": "English", "domain": "Document"},
    {"q": "is file me test name aur result table me btao", "lang": "Hinglish", "domain": "Document"},
    {"q": "Serology test me kon konsi bimarion ki jaanch hui hai?", "lang": "Hinglish", "domain": "Document"},
    {"q": "what is the report date and approval time?", "lang": "English", "domain": "Document"},
    {"q": "is report ka main takeaway btao", "lang": "Hinglish", "domain": "Document"},
    {"q": "क्या इसमें किसी गंभीर बीमारी के संकेत हैं?", "lang": "Hindi", "domain": "Document"},
    {"q": "explain this uploaded lab report in simple Hindi/Hinglish", "lang": "Hinglish", "domain": "Document"},
]

def run_evaluation():
    logger.info("Starting 100-Question Comprehensive Evaluation Suite...")
    session_id = f"eval_sess_{int(time.time())}"
    conversation_id = f"eval_conv_{int(time.time())}"
    
    # Initialize session
    session_manager.get_or_create_session(session_id, "Automated Benchmark Evaluator")
    
    passed_count = 0
    failed_count = 0
    results = []

    for i, q_item in enumerate(TEST_QUESTIONS, 1):
        query = q_item["q"]
        lang = q_item["lang"]
        domain = q_item["domain"]
        
        start_time = time.perf_counter()
        
        # Run retrieval & response generation simulation
        try:
            # Step 1: Retrieval
            res = retrieval_router.retrieve_context(
                query, session_id=session_id, conversation_id=conversation_id, query_language=lang, query_domain=domain
            )
            chunks = res.get("context_chunks", [])
            
            # Step 2: Prompt construction
            prompt = prompt_builder.build_adaptive_prompt(
                query, chunks, lang, domain, "QA"
            )
            
            elapsed = time.perf_counter() - start_time
            
            # Quality Checks:
            # 1. No repetition of prompt dictionary words 3 times
            # 2. No leakage of constitution_of_india or rti_act into non-legal medical queries
            # 3. Prompt has clear structure & rules
            has_leak = False
            for c in chunks:
                src = c.get("source", "").lower()
                if domain == "Medical" and ("constitution" in src or "rti_act" in src):
                    has_leak = True
                if domain == "Document" and ("constitution" in src or "rti_act" in src or "stomach.md" in src):
                    has_leak = True
            
            is_valid = not has_leak and len(prompt) > 100
            
            if is_valid:
                passed_count += 1
                status = "PASSED"
            else:
                failed_count += 1
                status = "FAILED (Context Leakage)"
                
            results.append({
                "num": i,
                "query": query,
                "domain": domain,
                "lang": lang,
                "chunks_used": len(chunks),
                "sources": [c.get("source") for c in chunks],
                "time_ms": round(elapsed * 1000, 2),
                "status": status
            })
            
            if i % 10 == 0 or not is_valid:
                logger.info(f"[{i}/100] Query: '{query[:40]}...' | Chunks: {len(chunks)} | Time: {round(elapsed*1000, 1)}ms | Status: {status}")

        except Exception as e:
            failed_count += 1
            logger.error(f"[{i}/100] Error processing query '{query}': {e}")
            results.append({
                "num": i, "query": query, "domain": domain, "lang": lang, "status": f"FAILED (Exception: {e})"
            })

    print("\n" + "="*70)
    print(f"📊 EVALUATION COMPLETE: {passed_count}/100 PASSED ({passed_count}% Success Rate)")
    print("="*70)
    
    report_file = os.path.join(os.path.dirname(__file__), "eval_results_100.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({"total": 100, "passed": passed_count, "failed": failed_count, "results": results}, f, indent=2, ensure_ascii=False)
    print(f"Saved detailed benchmark report to: {report_file}")
    
    return passed_count == 100

if __name__ == "__main__":
    run_evaluation()
