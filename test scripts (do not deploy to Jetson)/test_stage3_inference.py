import os
import sys
import time
import requests

# Reconfigure stdout/stderr to UTF-8 for Windows console support of Devanagari/Hindi printing
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure workspace is in search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import llm_inference
import telemetry
import session_manager
import kb_pipeline
import retrieval_router

def preflight_check():
    """
    Validates Ollama endpoint is active and llama3.2:1b model is ready.
    Avoids crashing with unhandled ConnectionError.
    """
    print("=================== RUNNING OLLAMA PRE-FLIGHT CHECK ===================")
    url = "http://localhost:11434/api/tags"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        models = [m["name"] for m in data.get("models", [])]
        
        # Check for model substring/exact match
        model_found = any("llama3.2:1b" in m for m in models)
        if not model_found:
            print("\n[PRE-FLIGHT ERROR] Ollama is active, but model 'llama3.2:1b' is not pulled.")
            print("Please run: ollama pull llama3.2:1b")
            sys.exit(1)
        print("Pre-flight check passed: 'llama3.2:1b' is pulled and ready.\n")
    except requests.exceptions.RequestException as e:
        print("\n[PRE-FLIGHT ERROR] Ollama service is not running on http://localhost:11434.")
        print(f"Details: {e}")
        print("Please start Ollama and ensure 'llama3.2:1b' is pulled.")
        sys.exit(1)

def run_scenario(query, name, session_id):
    """Helper to run a query stream, assert event sequences, and return metrics."""
    print(f"\n--- Scenario: {name} ---")
    print(f"Query: {query}")
    
    stream = llm_inference.generate_answer_stream(query, session_id)
    events = list(stream)
    
    # Check if we triggered the no-context case
    first_event = events[0] if events else {}
    if "skipped_llm" in first_event:
        print("Bypassed LLM (No-Context Case)")
        assert first_event["skipped_llm"] is True
        assert first_event["has_context"] is False
        assert len(first_event["citations"]) == 0
        return {
            "query": query,
            "lang": llm_inference.detect_response_language(query),
            "chunks": 0,
            "tokens": 0,
            "tps": 0.0,
            "citations": 0,
            "status": "PASS (Skipped LLM)"
        }
        
    # Standard streaming flow
    token_events = [e for e in events if e.get("type") == "token"]
    citation_events = [e for e in events if e.get("type") == "citation"]
    done_events = [e for e in events if e.get("type") == "done"]
    
    # Assertions
    assert len(token_events) > 0, "Expected at least one token event"
    assert len(citation_events) == 1, "Expected exactly one citation event"
    assert len(done_events) == 1, "Expected exactly one done event"
    
    # Check streaming property: tokens should be yielded individually
    tokens_text = [e["data"]["token"] for e in token_events]
    assembled_answer = "".join(tokens_text)
    print(f"Tokens streamed: {len(token_events)} chunks.")
    print(f"Assembled Answer preview: {assembled_answer[:120]}...")
    
    citations = citation_events[0]["data"]["citations"]
    print(f"Citations mapped: {len(citations)} sources.")
    for cit in citations:
        print(f"  - [{cit['index']}] {cit['filename']}, Page {cit['page_number']} ({cit['domain']})")
        
    done_data = done_events[0]["data"]
    print(f"Telemetry metrics: {done_data['total_tokens']} tokens in {done_data['generation_time_ms']}ms ({done_data['tokens_per_second']:.2f} tokens/sec)")
    
    assert done_data["total_tokens"] > 0
    assert done_data["generation_time_ms"] > 0
    assert done_data["tokens_per_second"] > 0.0
    
    lang = llm_inference.detect_response_language(query)
    total_chunks = done_data["user_doc_chunks_used"] + done_data["knowledge_base_chunks_used"]
    
    return {
        "query": query,
        "lang": lang,
        "chunks": total_chunks,
        "tokens": done_data["total_tokens"],
        "tps": done_data["tokens_per_second"],
        "citations": len(citations),
        "status": "PASS"
    }

def test_inference_suite():
    # 1. Run Pre-flight Check
    preflight_check()
    
    # 2. Init database schemas
    kb_pipeline.init_directories()
    session_manager.init_session_db()
    telemetry.init_telemetry_db()
    
    results = []
    
    # Scenario 1: KYC English Query (Retrieved context)
    s1_query = "What is the procedure for verification of customer identity under KYC guidelines?"
    res1 = run_scenario(s1_query, "KYC Query (English)", session_id=None)
    results.append(res1)
    
    # Scenario 2: Hindi circular Query (Glossary and language detected as Hindi)
    s2_query = "भारत का संविधान क्या है?"
    res2 = run_scenario(s2_query, "Constitution Query (Hindi)", session_id=None)
    results.append(res2)
    
    # Scenario 3: Off-topic query (No context fallback)
    s3_query = "purple elephants jumping on Mars drinking tea"
    res3 = run_scenario(s3_query, "Off-topic Query (No Context)", session_id=None)
    results.append(res3)
    
    # 3. Print Summary Report Table
    print("\n=========================================================================================================")
    print("                                     STAGE 3 LLM INFERENCE TEST SUMMARY                                  ")
    print("=========================================================================================================")
    print(f"| {'Query (truncated)':30} | {'Lang':7} | {'Chunks':6} | {'Tokens':6} | {'Tok/Sec':8} | {'Cites':5} | {'Status':16} |")
    print("---------------------------------------------------------------------------------------------------------")
    for r in results:
        q_trunc = r["query"][:27] + "..." if len(r["query"]) > 30 else r["query"].ljust(30)
        print(f"| {q_trunc:30} | {r['lang']:7} | {r['chunks']:6d} | {r['tokens']:6d} | {r['tps']:8.2f} | {r['citations']:5d} | {r['status']:16} |")
    print("=========================================================================================================\n")
    
    # 4. Assert recent telemetry log insertion
    recent = telemetry.get_recent_telemetry(n=5)
    print(f"Telemetry database contains {len(recent)} recent records.")
    assert len(recent) >= 3, "Expected at least 3 telemetry records logged in SQLite"
    print("Telemetry database validation successful.")
    
    print("\nALL STAGE 3 INFERENCE TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        test_inference_suite()
    except AssertionError as ae:
        print(f"\n[TEST FAILURE] Assertion triggered: {ae}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[TEST ERROR] Unexpected crash: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
