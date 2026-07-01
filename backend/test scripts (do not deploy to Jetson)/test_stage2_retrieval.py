import os
import sys
import uuid
import docx
import shutil

# Ensure current directory is in search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import kb_pipeline
import session_manager
import retrieval_router

def create_test_docx(filename, paragraphs):
    """Helper to create a small DOCX file using python-docx."""
    if os.path.exists(filename):
        os.remove(filename)
    doc = docx.Document()
    for p in paragraphs:
        doc.add_paragraph(p)
    doc.save(filename)

def run_tests():
    print("=================== STARTING STAGE 2 RETRIEVAL TESTS ===================\n")
    
    # Initialize environment
    kb_pipeline.init_directories()
    session_manager.init_session_db()
    
    temp_dir = "./test_temp_retrieval"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Keep track of results for printing at the end
    results_summary = []
    
    # ----------------------------------------------------
    # Test Scenario 1: Query with no session_id (falls back to KB only)
    # ----------------------------------------------------
    print("--- Scenario 1: Query with no session_id ---")
    query_1 = "What is the procedure for verification of customer identity under KYC?"
    res_1 = retrieval_router.retrieve_context(query_1, session_id=None)
    
    assert res_1["has_any_context"] is True, "Expected to retrieve context from knowledge_base"
    assert res_1["user_doc_chunks_used"] == 0, "Expected 0 chunks from user_docs"
    assert res_1["knowledge_base_chunks_used"] > 0, "Expected chunks from knowledge_base"
    
    top_score_1 = res_1["context_chunks"][0]["similarity_score"] if res_1["context_chunks"] else 0.0
    results_summary.append({
        "type": "No Session (KB only)",
        "query": query_1,
        "expanded": res_1["expanded_query"][:35] + "...",
        "user_chunks": res_1["user_doc_chunks_used"],
        "kb_chunks": res_1["knowledge_base_chunks_used"],
        "top_score": top_score_1,
        "status": "PASS"
    })
    print("Scenario 1 passed.\n")
    
    # ----------------------------------------------------
    # Test Scenario 2: Ingest a unique fact, query, and verify priority
    # ----------------------------------------------------
    print("--- Scenario 2: User Doc ingestion and priority ranking ---")
    session_a = f"session_{uuid.uuid4().hex[:8]}"
    session_manager.get_or_create_session(session_a)
    
    # Create and ingest a mock docx containing a highly unique fact not in the knowledge_base
    docx_path = os.path.join(temp_dir, "rohit_account.docx")
    unique_fact = "Account number X-999-777 belongs to user Rohit Kumar and is currently active."
    create_test_docx(docx_path, [
        unique_fact,
        "Interest rate for this account is 6.5% per annum."
    ])
    
    # Ingest document
    ingest_res = kb_pipeline.ingest_user_document(docx_path, "rohit_account.docx", session_a, domain_hint="banking")
    doc_id = ingest_res["document_id"]
    print(f"Ingested mock document {doc_id} under session {session_a}")
    
    # Query for the unique fact
    query_2 = "Who does account number X-999-777 belong to?"
    res_2 = retrieval_router.retrieve_context(query_2, session_a)
    
    # Assertions
    assert res_2["has_any_context"] is True, "Expected to retrieve context"
    assert res_2["user_doc_chunks_used"] > 0, "Expected context from user_docs"
    
    # Assert that user_docs chunk is ranked first (above all knowledge_base chunks)
    first_chunk = res_2["context_chunks"][0]
    assert first_chunk["collection"] == "user_docs", f"Expected top chunk to come from user_docs, got {first_chunk['collection']}"
    assert "Rohit" in first_chunk["text"], f"Expected top chunk to contain unique fact about Rohit, got: {first_chunk['text']}"
    
    top_score_2 = res_2["context_chunks"][0]["similarity_score"] if res_2["context_chunks"] else 0.0
    results_summary.append({
        "type": "User Doc Priority",
        "query": query_2,
        "expanded": res_2["expanded_query"][:35] + "...",
        "user_chunks": res_2["user_doc_chunks_used"],
        "kb_chunks": res_2["knowledge_base_chunks_used"],
        "top_score": top_score_2,
        "status": "PASS"
    })
    print("Scenario 2 passed.\n")
    
    # ----------------------------------------------------
    # Test Scenario 3: Hinglish Glossary query and hospital domain retrieval
    # ----------------------------------------------------
    print("--- Scenario 3: Hinglish glossary expansion ---")
    query_3 = "cashless claim settlement reimbursement master circular on health insurance business bukhar"
    res_3 = retrieval_router.retrieve_context(query_3, session_id=None)
    
    # Check that expansion was applied (e.g. contains clinical equivalents like 'fever' or 'pyrexia')
    assert "fever" in res_3["expanded_query"].lower() or "pyrexia" in res_3["expanded_query"].lower(), \
        f"Expected expanded query to contain 'fever' or 'pyrexia', got: {res_3['expanded_query']}"
        
    assert res_3["has_any_context"] is True, "Expected context chunks"
    
    # Verify that hospital-domain chunks are retrieved
    hospital_chunks = [c for c in res_3["context_chunks"] if c["domain"] == "hospital"]
    assert len(hospital_chunks) > 0, "Expected to retrieve at least one hospital-domain chunk"
    
    top_score_3 = res_3["context_chunks"][0]["similarity_score"] if res_3["context_chunks"] else 0.0
    results_summary.append({
        "type": "Glossary Expansion",
        "query": query_3,
        "expanded": res_3["expanded_query"][:35] + "...",
        "user_chunks": res_3["user_doc_chunks_used"],
        "kb_chunks": res_3["knowledge_base_chunks_used"],
        "top_score": top_score_3,
        "status": "PASS"
    })
    print("Scenario 3 passed.\n")
    
    # ----------------------------------------------------
    # Test Scenario 4: Nonsense/Off-topic query rejection
    # ----------------------------------------------------
    print("--- Scenario 4: Nonsense query rejection ---")
    query_4 = "purple elephants jumping on Mars drinking tea"
    res_4 = retrieval_router.retrieve_context(query_4, session_id=None)
    
    # Assertions
    assert res_4["has_any_context"] is False, f"Expected has_any_context == False, got {len(res_4['context_chunks'])} chunks"
    assert len(res_4["context_chunks"]) == 0, "Expected empty context list"
    
    results_summary.append({
        "type": "Nonsense Rejection",
        "query": query_4,
        "expanded": res_4["expanded_query"][:35] + "...",
        "user_chunks": res_4["user_doc_chunks_used"],
        "kb_chunks": res_4["knowledge_base_chunks_used"],
        "top_score": 0.0,
        "status": "PASS"
    })
    print("Scenario 4 passed.\n")
    
    # Clean up temp test files
    shutil.rmtree(temp_dir)
    
    # ----------------------------------------------------
    # Print Summary Table
    # ----------------------------------------------------
    print("=========================================================================================================")
    print("                                     STAGE 2 RETRIEVAL TEST SUMMARY                                      ")
    print("=========================================================================================================")
    print(f"| {'Query Type':24} | {'Expanded Query (truncated)':32} | {'User Chunks':11} | {'KB Chunks':9} | {'Top Sim':8} | {'Status':6} |")
    print("---------------------------------------------------------------------------------------------------------")
    for r in results_summary:
        print(f"| {r['type']:24} | {r['expanded']:32} | {r['user_chunks']:11d} | {r['kb_chunks']:9d} | {r['top_score']:8.4f} | {r['status']:6} |")
    print("=========================================================================================================\n")
    print("ALL STAGE 2 TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    try:
        run_tests()
    except AssertionError as ae:
        print(f"\nAssertionError triggered: {ae}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
