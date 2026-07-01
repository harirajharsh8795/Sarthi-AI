import os
import sys
import pytest
from fastapi.testclient import TestClient

# Add parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from intent_service import intent_service
from rewrite_service import rewrite_service
from query_planner import query_planner
from ranking_service import ranking_service
from graph_service import graph_service
from compression_service import compression_service
from prompt_builder import prompt_builder
from confidence_service import confidence_service
from validation_service import validation_service
from followup_service import followup_service

client = TestClient(app)

def test_intent_detection():
    """Checks query understanding classifications (English/Hindi, domain, type)."""
    # Test English Medical
    c1 = intent_service.classify_query("I have a high fever and headache, what should I do?")
    assert c1["language"] == "English"
    assert c1["domain"] == "Medical"
    
    # Test Hindi Banking
    c2 = intent_service.classify_query("मेरा खाता बंद हो गया है kyc कैसे करें?")
    assert c2["language"] in ["Hindi", "Hinglish"]
    assert c2["domain"] == "Banking"

def test_query_rewriting():
    """Checks follow-up pronoun rewriting."""
    history = [
        {"role": "user", "content": "What are the RBI KYC guidelines?"},
        {"role": "assistant", "content": "RBI KYC guidelines mandate periodic updates of official identity documents."}
    ]
    # Mock requests.post call to avoid external dependency slow responses
    from unittest.mock import patch, MagicMock
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"response": "Explain RBI KYC guidelines details"}
    
    with patch("requests.post", return_value=mock_resp):
        rewritten = rewrite_service.rewrite_query("explain them more", history)
        assert rewritten != "explain them more"
        assert "rbi" in rewritten.lower() or "kyc" in rewritten.lower()

def test_query_planning():
    """Checks decomposition of compound questions."""
    plan = query_planner.plan_query("Explain PMJAY eligibility and list the required documents")
    assert len(plan) >= 1
    # Check plan format
    assert "task_id" in plan[0]
    assert "description" in plan[0]
    assert "query_terms" in plan[0]

def test_hybrid_ranking_and_metrics():
    """Validates trust weights and MRR/NDCG retrieval benchmark formulas."""
    chunks = [
        {"source": "rbi_kyc_guideline.pdf", "text": "PAN card is mandatory for bank account opening.", "page_number": 2, "domain": "Banking", "collection": "knowledge_base", "similarity_score": 0.8},
        {"source": "user_doc.pdf", "text": "This is user uploaded statement doc.", "page_number": 1, "domain": "Banking", "collection": "user_docs", "similarity_score": 0.7},
        {"source": "random_website.txt", "text": "Random blog post about banking tips.", "page_number": 1, "domain": "General", "collection": "knowledge_base", "similarity_score": 0.4}
    ]
    
    reranked = ranking_service.rerank_chunks("kyc documents", chunks)
    assert len(reranked) == 3
    # First chunk should have the highest trust score (RBI = 0.98, user = 0.95, random = 0.90)
    assert reranked[0]["trust_score"] == 0.98
    
    # Check IR benchmarking calculations
    benchmarks = ranking_service.evaluate_retrieval_benchmarks(reranked, threshold=0.6)
    assert "precision" in benchmarks
    assert "mrr" in benchmarks
    assert "ndcg" in benchmarks
    assert benchmarks["mrr"] > 0.0

def test_knowledge_graph_extraction():
    """Checks Entity-Relation JSON triple extraction patterns."""
    text = "RBI issues KYC Guidelines for commercial banks. KYC requires PAN Card."
    triples = graph_service.extract_knowledge_graph(text, use_llm=False)
    assert len(triples) >= 1
    assert "subject" in triples[0]
    assert "relation" in triples[0]
    assert "object" in triples[0]

def test_context_compression():
    """Checks merging of overlapping strings."""
    chunks = [
        {"source": "doc1.pdf", "page_number": 1, "text": "The patient complained of a severe headache and body fatigue.", "hybrid_score": 0.8, "index": 1},
        {"source": "doc1.pdf", "page_number": 1, "text": "severe headache and body fatigue. Patient was advised bedrest.", "hybrid_score": 0.7, "index": 2}
    ]
    res = compression_service.compress_context(chunks)
    assert res["ratio"] < 1.0
    comp_text = res["compressed_chunks"][0]["text"]
    assert "advised bedrest" in comp_text

def test_confidence_calibration():
    """Checks multi-factor confidence percentage output."""
    chunks = [
        {"source": "govt_rules.pdf", "page_number": 1, "text": "Fact detail here.", "hybrid_score": 0.85, "trust_score": 1.0, "domain": "Legal"}
    ]
    conf = confidence_service.calculate_confidence(chunks, "Legal", citations_used_count=1)
    assert conf["confidence_score"] > 50
    assert "confidence_label" in conf

def test_citation_validator_and_self_eval():
    """Verifies citation matching grounding score calculation."""
    chunks = [
        {"source": "rbi.pdf", "page_number": 2, "text": "PAN card is required.", "index": 1}
    ]
    answer = "To open an account, a PAN card is required [1]. Also we need some other unmentioned proof."
    res = validation_service.validate_citations(answer, chunks)
    assert "grounding_score" in res
    assert len(res["unsupported_sentences"]) >= 1 # The second sentence has no overlap grounding
    
    # Self Eval
    se = validation_service.evaluate_response_self(res["validated_answer"], chunks, res["grounding_score"])
    assert se["hallucination_risk"] in ["High", "Medium", "Low"]

def test_followup_question_generator():
    """Checks generation of domain specific suggestions."""
    questions = followup_service.generate_followup_rules("Banking", "English")
    assert len(questions) >= 3
    assert any("kyc" in q.lower() or "document" in q.lower() for q in questions)
