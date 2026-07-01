import re
import time
import json
import logging
import requests
from typing import Generator

import retrieval_router
import session_manager
import telemetry
from config import settings
from intent_service import intent_service
from rewrite_service import rewrite_service
from query_planner import query_planner
from ranking_service import ranking_service
from multihop_service import multihop_service
from graph_service import graph_service
from compression_service import compression_service
from prompt_builder import prompt_builder
from confidence_service import confidence_service
from validation_service import validation_service
from post_processor import post_processor
from followup_service import followup_service

OLLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = settings.LLM_MODEL_NAME

def generate_answer_stream(
    query: str, 
    session_id: str | None, 
    response_language: str | None = None, 
    conversation_id: str | None = None
) -> Generator[dict, None, None]:
    """
    Cognitive RAG Answer Generation Pipeline:
    1. Language, domain, and intent classification.
    2. standalone query rewriting.
    3. Query planning (decomposing compound prompts).
    4. Multi-hop retrieval loop & hybrid reranking.
    5. Entity-relation JSON triples graph extraction.
    6. Context compression and chunk deduplication.
    7. Adaptive prompt building.
    8. Ollama token streaming.
    9. Citation validation and self-evaluation checks.
    10. Follow-up suggestions generation.
    11. Log metrics and yield diagnostic inspector.
    """
    start_time = time.perf_counter()
    
    # 1. Query Understanding
    classification = intent_service.classify_query(query)
    lang = response_language or classification["language"]
    domain = classification["domain"]
    intent = classification["intent"]
    
    # 2. Query Rewriting
    history = []
    if session_id and conversation_id:
        try:
            history = session_manager.get_conversation_messages(conversation_id)
        except Exception:
            pass
    rewritten_query = rewrite_service.rewrite_query(query, history)
    
    # Redact PII
    from privacy_engine import privacy_engine
    query = privacy_engine.redact_pii(query)
    rewritten_query = privacy_engine.redact_pii(rewritten_query)
    
    # 3. Query Planning
    plan = query_planner.plan_query(rewritten_query)
    
    # 4. Multi-hop Retrieval & Hybrid Reranking
    start_retrieval = time.perf_counter()
    context_chunks = multihop_service.retrieve_multihop(plan, session_id or "", conversation_id)
    
    # Isolation Guard Verification
    from isolation_guard import isolation_guard
    from audit_service import audit_trail_service
    from logger_config import log_context
    isolated_chunks = []
    for c in context_chunks:
        if isolation_guard.verify_document_isolation(c, session_id or "", conversation_id):
            isolated_chunks.append(c)
        else:
            audit_trail_service.log_event(
                event_type="isolation_leak_blocked",
                details=f"Cross-session access blocked for document: {c.get('source')}",
                result="BLOCKED",
                severity="HIGH",
                request_id=getattr(log_context, "request_id", "GLOBAL"),
                conversation_id=conversation_id
            )
    context_chunks = isolated_chunks
    
    retrieval_duration = time.perf_counter() - start_retrieval
    
    # Benchmark retrieval
    eval_metrics = ranking_service.evaluate_retrieval_benchmarks(context_chunks)
    
    # Add numerical index identifiers for citation formatting
    for idx, c in enumerate(context_chunks, 1):
        c["index"] = idx

    user_doc_chunks_used = sum(1 for c in context_chunks if c["collection"] == "user_docs")
    knowledge_base_chunks_used = sum(1 for c in context_chunks if c["collection"] == "knowledge_base")
    
    # Check threshold guard
    SKIP_LLM_THRESHOLD = 0.52
    max_sim = max([c.get("hybrid_score", 0.0) for c in context_chunks]) if context_chunks else 0.0
    has_user_doc_chunks = user_doc_chunks_used > 0
    
    # Check medical domain alignment
    query_lower = query.lower()
    medical_keywords = ["bukhar", "fever", "bimari", "dawai", "dawa", "ilaj", "symptoms", "pain", "dard"]
    is_medical_query = any(k in query_lower for k in medical_keywords)
    domain_mismatch = is_medical_query and not has_user_doc_chunks and all(c.get("domain") != "hospital" for c in context_chunks)
    
    if (max_sim < SKIP_LLM_THRESHOLD or domain_mismatch) and not has_user_doc_chunks:
        # Fallback text
        if lang == "Hindi":
            fallback_text = (
                "इस विषय पर मेरे दस्तावेज़ों में विश्वसनीय जानकारी नहीं मिली। "
                "कृपया संबंधित दस्तावेज़ अपलोड करके प्रश्न पूछें।"
            )
        else:
            fallback_text = (
                "I could not find reliable information about this topic in my document library. "
                "You can upload a relevant document and ask me questions about it."
            )
            
        yield {"type": "token", "data": {"token": fallback_text}}
        yield {"type": "citation", "data": {"citations": []}}
        
        # Telemetry for skipped RAG
        telemetry.log_inference(
            session_id=session_id, query=query, expanded_query=rewritten_query, response_language=lang,
            has_context=False, skipped_llm=True, user_doc_chunks_used=0, knowledge_base_chunks_used=0,
            total_chunks_in_prompt=0, total_tokens_generated=0, generation_time_ms=0, tokens_per_second=0.0,
            model_name=MODEL_NAME, intent=intent, detected_domain=domain
        )
        return

    # 5. Knowledge Graph Triples extraction
    start_graph = time.perf_counter()
    graph_triples = graph_service.extract_knowledge_graph(rewritten_query, use_llm=False)
    
    # 6. Context Compression
    start_compression = time.perf_counter()
    compression_res = compression_service.compress_context(context_chunks)
    compressed_chunks = compression_res["compressed_chunks"]
    compression_duration = time.perf_counter() - start_compression
    
    # 7. Adaptive Prompt Building
    prompt = prompt_builder.build_adaptive_prompt(
        rewritten_query, compressed_chunks, lang, domain, intent, plan, graph_triples
    )
    
    # 8. Local LLM streaming
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
            "num_ctx": 2048,
            "num_predict": 512
        }
    }
    
    full_text = ""
    total_tokens = 0
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                token = data.get("response", "")
                full_text += token
                total_tokens += 1
                
                yield {
                    "type": "token",
                    "data": {"token": token}
                }
                
                if data.get("done", False):
                    break
    except Exception as e:
        logging.error(f"Inference calling failed: {e}")
        yield {
            "type": "error",
            "data": {"message": f"Inference error: {str(e)}"}
        }

    generation_time_sec = time.perf_counter() - start_time
    generation_time_ms = int(generation_time_sec * 1000)
    
    # 9. Citation Validation & Self-Evaluation
    validation_res = validation_service.validate_citations(full_text, context_chunks)
    validated_text = validation_res["validated_answer"]
    
    from output_validator import output_validator
    validated_text = output_validator.validate_and_refine_output(validated_text, context_chunks)
    
    grounding_score = validation_res["grounding_score"]
    
    # Count validated citations list
    citations_used = []
    seen_indices = set()
    matches = re.findall(r'\[(\d+)\]', validated_text)
    
    for match in matches:
        try:
            idx = int(match)
            if idx in seen_indices:
                continue
            if 1 <= idx <= len(context_chunks):
                chunk = context_chunks[idx - 1]
                citations_used.append({
                    "index": idx,
                    "filename": chunk["source"],
                    "page_number": chunk["page_number"],
                    "domain": chunk["domain"],
                    "collection": chunk["collection"]
                })
                seen_indices.add(idx)
        except ValueError:
            pass

    # Yield valid citations list to frontend
    yield {
        "type": "citation",
        "data": {
            "citations": citations_used
        }
    }
    
    # Self-Evaluation
    self_eval = validation_service.evaluate_response_self(validated_text, context_chunks, grounding_score)
    
    # 10. Confidence Calibration
    conf_res = confidence_service.calculate_confidence(context_chunks, domain, len(citations_used))
    
    # 11. Follow-up Suggestions
    start_followups = time.perf_counter()
    followups = followup_service.generate_followups(rewritten_query, validated_text, domain, lang)
    followup_duration = time.perf_counter() - start_followups
    
    # Telemetry Log
    tokens_per_second = (total_tokens / generation_time_sec) if generation_time_sec > 0 else 0.0
    
    inference_id = telemetry.log_inference(
        session_id=session_id, query=query, expanded_query=rewritten_query, response_language=lang,
        has_context=len(citations_used) > 0, skipped_llm=False, 
        user_doc_chunks_used=user_doc_chunks_used, knowledge_base_chunks_used=knowledge_base_chunks_used,
        total_chunks_in_prompt=len(compressed_chunks), total_tokens_generated=total_tokens,
        generation_time_ms=generation_time_ms, tokens_per_second=tokens_per_second, model_name=MODEL_NAME,
        intent=intent, detected_domain=domain, rewritten_query=rewritten_query,
        query_plan=json.dumps(plan), confidence_score=conf_res["confidence_score"],
        confidence_label=conf_res["confidence_label"], grounding_score=grounding_score,
        citation_coverage=len(citations_used)/len(context_chunks) if context_chunks else 0.0,
        self_eval_summary=self_eval["eval_summary"], retrieval_mrr=eval_metrics["mrr"],
        retrieval_ndcg=eval_metrics["ndcg"], knowledge_graph=json.dumps(graph_triples)
    )
    
    if session_id:
        session_manager.get_or_create_session(session_id)
        
    # Yield done event compatible with legacy parser
    yield {
        "type": "done",
        "data": {
            "total_tokens": total_tokens,
            "generation_time_ms": generation_time_ms,
            "tokens_per_second": tokens_per_second,
            "user_doc_chunks_used": user_doc_chunks_used,
            "knowledge_base_chunks_used": knowledge_base_chunks_used,
            "session_id": session_id,
            "has_context": len(citations_used) > 0,
            "response_language": lang,
            
            # Stage 2 metadata variables
            "inference_id": inference_id,
            "followups": followups,
            "confidence_score": conf_res["confidence_score"],
            "confidence_label": conf_res["confidence_label"],
            "grounding_score": grounding_score
        }
    }
