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
from logger_config import logger

OLLAMA_URL = settings.OLLAMA_URL
MODEL_NAME = settings.LLM_MODEL_NAME

def detect_response_language(text: str) -> str:
    """Detects the language of the query using intent_service."""
    return intent_service.detect_language(text)

def generate_answer_stream(query: str, session_id: str | None, response_language: str | None = None, conversation_id: str | None = None) -> Generator[dict, None, None]:
    try:
        yield from _generate_answer_stream_inner(query, session_id, response_language, conversation_id)
    except Exception as e:
        import traceback
        import logging
        logging.getLogger(__name__).error(f"Stream generation error: {e}\n{traceback.format_exc()}")
        yield {"type": "error", "data": {"message": f"Something went wrong while generating the response.\n\nError: {str(e)}" }}
        return

def _generate_answer_stream_inner(
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
    
    # 0. Prompt Security Scan
    from prompt_guard import PromptGuard
    guard = PromptGuard()
    guard_res = guard.scan_query(query)
    if guard_res["blocked"]:
        logger.warning(f"Query blocked by PromptGuard: {guard_res['reason']}")
        yield {"type": "token", "data": {"token": f"⚠️ Security Notice: Query could not be processed because it contains prohibited pattern vectors ({guard_res['reason']})."}}
        yield {"type": "done", "data": {}}
        return

    # 1. Query Understanding
    import uuid
    if conversation_id:
        user_msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        try:
            session_manager.save_message(user_msg_id, conversation_id, "user", query)
        except Exception as e:
            logger.error(f"Failed to save user message: {e}")

    classification = intent_service.classify_query(query)
    lang = classification["language"]
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
    context_chunks = multihop_service.retrieve_multihop(plan, session_id or "", conversation_id, query_language=lang, original_query=query)
    
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
    SKIP_LLM_THRESHOLD = 0.22
    max_sim = max([c.get("hybrid_score") or c.get("similarity_score", 0.0) for c in context_chunks]) if context_chunks else 0.0
    has_user_doc_chunks = user_doc_chunks_used > 0
    
    # Check medical domain alignment (support both 'medical' and 'hospital' domains)
    query_lower = query.lower()
    medical_keywords = ["bukhar", "bhukar", "bhukhar", "bukhaar", "fever", "bimari", "bimaari", "dawai", "dvai", "dvaii", "dawa", "ilaj", "symptoms", "pain", "dard", "dengue", "malaria", "cough", "khansi", "doctor", "hospital", "report", "prescription", "goli", "condom", "sex", "libido"]
    is_medical_query = any(k in query_lower for k in medical_keywords)
    domain_mismatch = is_medical_query and not has_user_doc_chunks and all(c.get("domain") not in ("hospital", "medical") for c in context_chunks)
    
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
            
        yield {"skipped_llm": True, "has_context": False, "citations": []}
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

    # Limit context chunks to top 4 for optimal grounding and inference speed
    context_chunks = context_chunks[:4]

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
    prompt = f"IMPORTANT: You MUST respond ONLY in {lang}. Do not switch languages under any circumstances.\n\n" + prompt
    
    # Sanitize user query string (strip trailing slashes that break string formatting)
    query = query.strip().rstrip('\\').rstrip('/').strip()

    # 8. Local LLM streaming with maximum speed optimizations (greedy temperature 0.0)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.0,
            "top_p": 0.9,
            "num_ctx": 1024,
            "num_predict": 450,
            "repeat_penalty": 1.15
        }
    }
    
    full_text = ""
    total_tokens = 0
    token_buffer = ""
    
    try:
        response = requests.post(settings.OLLAMA_URL, json=payload, stream=True, timeout=120)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                token = data.get("response", "")
                full_text += token
                total_tokens += 1
                token_buffer += token
                
                # Buffer tokens slightly (2-3 chars or word boundaries) to deliver smooth SSE streaming without micro-lag
                if len(token_buffer) >= 3 or " " in token_buffer or "\n" in token_buffer or data.get("done", False):
                    yield {
                        "type": "token",
                        "data": {"token": token_buffer}
                    }
                    token_buffer = ""
                
                if data.get("done", False):
                    if token_buffer:
                        yield {
                            "type": "token",
                            "data": {"token": token_buffer}
                        }
                        token_buffer = ""
                    break
    except Exception as e:
        import traceback
        logger.error(f"Ollama inference failed: {e}\n{traceback.format_exc()}")
        yield {"type": "error", "data": {"message": "Inference failed to connect to the model."}}
        return
        
    generation_time_ms = (time.perf_counter() - start_time) * 1000
    tokens_per_second = total_tokens / (generation_time_ms / 1000) if generation_time_ms > 0 else 0.0

    logger.debug(f"DEBUG: Assembled text prefix (200 chars): {full_text[:200]!r}")
    logger.debug(f"DEBUG: Context chunks count: {len(context_chunks)}")
    
    # 9. Citation Validation & Self-Evaluation
    try:
        validation_res = validation_service.validate_citations(full_text, context_chunks, query)
        validated_text = validation_res["validated_text"]
        
        from output_validator import output_validator
        validated_text = output_validator.validate_and_refine_output(validated_text, context_chunks)
        
        grounding_score = validation_res["grounding_score"]
    except Exception as e:
        logger.error(f"Validation failed, using raw output: {e}")
        validated_text = full_text
        grounding_score = 0.0

    # Count validated citations list
    citations_used = []
    seen_indices = set()
    try:
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
                        "collection": chunk["collection"],
                        "text_preview": chunk.get("text", "")
                    })
                    seen_indices.add(idx)
            except ValueError:
                pass

        # Fallback: if no explicit citations were generated by LLM but retrieval succeeded, map all context chunks
        if len(citations_used) == 0 and len(context_chunks) > 0:
            for idx, chunk in enumerate(context_chunks, 1):
                citations_used.append({
                    "index": idx,
                    "filename": chunk["source"],
                    "page_number": chunk["page_number"],
                    "domain": chunk["domain"],
                    "collection": chunk["collection"],
                    "text_preview": chunk.get("text", "")
                })
    except Exception as e:
        logger.error(f"Citation mapping failed: {e}")

    # Yield valid citations list to frontend
    yield {
        "type": "citation",
        "data": {
            "citations": citations_used
        }
    }
    
    # Self-Evaluation
    self_eval = {"eval_summary": "N/A"}
    try:
        self_eval = validation_service.evaluate_response_self(validated_text, context_chunks, grounding_score)
    except Exception as e:
        logger.error(f"Self-Evaluation failed: {e}")
    
    # 10. Confidence Calibration
    conf_res = {"confidence_score": 0.0, "confidence_label": "UNKNOWN"}
    try:
        conf_res = confidence_service.calculate_confidence(context_chunks, domain, len(citations_used))
    except Exception as e:
        logger.error(f"Confidence calibration failed: {e}")
    
    # 11. Follow-up Suggestions
    followups = []
    try:
        start_followups = time.perf_counter()
        followups = followup_service.generate_followups(rewritten_query, validated_text, domain, lang)
        followup_duration = time.perf_counter() - start_followups
    except Exception as e:
        logger.error(f"Follow-up generation failed: {e}")
    
    # Telemetry Log
    tokens_per_second = (total_tokens / (generation_time_ms / 1000)) if generation_time_ms > 0 else 0.0
    
    try:
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
    except Exception as e:
        logger.error(f"Telemetry logging failed: {e}")
    
    if session_id:
        session_manager.get_or_create_session(session_id)
        
    if conversation_id:
        import uuid
        asst_msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        try:
            session_manager.save_message(asst_msg_id, conversation_id, "assistant", validated_text, citations_used)
        except Exception as e:
            logger.error(f"Failed to save assistant message: {e}")
        
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
