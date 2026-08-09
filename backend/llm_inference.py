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

    # 1. Query Understanding & Conversation Resolution
    import uuid
    if session_id:
        conversation_id = session_manager.ensure_conversation_exists(conversation_id or "new", session_id, title=query[:100])

    if conversation_id:
        user_msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        try:
            session_manager.save_message(user_msg_id, conversation_id, "user", query, session_id=session_id or "default_session")
        except Exception as e:
            logger.error(f"Failed to save user message: {e}")

    classification = intent_service.classify_query(query)
    lang = classification["language"]
    domain = classification["domain"]
    intent = classification["intent"]
    
    # Language Selection Priority:
    # 1. Devanagari script in query -> FORCE Hindi.
    # 2. Query detected as Hinglish -> FORCE Hinglish.
    # 3. Query detected as English (pure ASCII/English words) -> FORCE English so English questions ALWAYS get English answers.
    # 4. Fallback to response_language UI toggle.
    detected_lang = intent_service.detect_language(query)
    if re.search(r'[\u0900-\u097f]', query):
        lang = "Hindi"
    elif detected_lang == "Hinglish":
        lang = "Hinglish"
    elif detected_lang == "English":
        lang = "English"
    elif response_language and response_language in ["English", "Hindi", "Hinglish"]:
        lang = response_language
    else:
        lang = classification.get("language", "English")
    
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
    context_chunks = multihop_service.retrieve_multihop(plan, session_id or "", conversation_id, query_language=lang, original_query=query, query_domain=domain)
    
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
    
    # Limit context chunks to top 4 for ultra-fast TTFT latency
    if context_chunks:
        context_chunks = context_chunks[:4]
    else:
        context_chunks = []


    # 5. Knowledge Graph Triples extraction
    start_graph = time.perf_counter()
    graph_triples = graph_service.extract_knowledge_graph(rewritten_query, use_llm=False)
    
    # 6. Context Compression
    start_compression = time.perf_counter()
    compression_res = compression_service.compress_context(context_chunks)
    compressed_chunks = compression_res["compressed_chunks"]
    compression_duration = time.perf_counter() - start_compression
    
    # ── CONTEXT WINDOW & RAM TRADEOFF JUSTIFICATION ──
    # Worst-case token estimation for a Devanagari Hindi query with 5 max-length context chunks:
    # - 5 chunks x ~512-800 characters of Devanagari text = ~3,000 characters = ~3,750 tokens (Devanagari BPE ratio 1.25 tokens/char)
    # - System instructions + rules + doc directive = ~300 tokens
    # - User query + conversational history = ~150 tokens
    # Total worst-case prompt = ~4,200 tokens (which silently truncated under default 2,048 num_ctx!).
    #
    # JETSON RAM TRADEOFF:
    # Llama 3.2 1B base weights require ~0.9 GB FP16 VRAM/RAM.
    # Increasing num_ctx to 4096 adds ~380 MB FP16 KV cache memory allocation.
    # Total runtime footprint is ~1.3-1.5 GB Unified Memory, which easily fits within the 8 GB RAM budget
    # of Jetson Orin Nano (leaving ~6.5 GB for OS, PyTorch embeddings, and UI).
    NUM_CTX = settings.LLM_NUM_CTX
    SAFE_TOKEN_LIMIT = int(NUM_CTX * 0.85)  # 85% of NUM_CTX for prompt safety margin

    # 7. Adaptive Prompt Building & Token Budget Safety Check
    def _assemble_prompt(chunks_to_use):
        p = prompt_builder.build_adaptive_prompt(
            rewritten_query, chunks_to_use, lang, domain, intent, plan, graph_triples
        )
        if lang == "Hinglish":
            return "IMPORTANT: Respond ONLY in natural, friendly Hinglish. Give a clear, helpful, well-structured answer.\n\n" + p
        else:
            return f"IMPORTANT: You MUST respond ONLY in {lang}. Do not switch languages under any circumstances.\n\n" + p

    prompt = _assemble_prompt(compressed_chunks)
    estimated_tokens = prompt_builder.estimate_token_count(prompt)

    # If prompt exceeds 85% of NUM_CTX, iteratively drop lowest-similarity context chunks first
    if estimated_tokens > SAFE_TOKEN_LIMIT and compressed_chunks:
        logger.warning(
            f"Prompt estimated tokens ({estimated_tokens}) exceeds 85% limit ({SAFE_TOKEN_LIMIT}) of num_ctx ({NUM_CTX}). "
            f"Truncating lowest-similarity context chunks."
        )
        sorted_by_score = sorted(compressed_chunks, key=lambda c: c.get("similarity_score", 0.0))
        while estimated_tokens > SAFE_TOKEN_LIMIT and len(compressed_chunks) > 1:
            lowest_chunk = sorted_by_score.pop(0)
            if lowest_chunk in compressed_chunks:
                compressed_chunks.remove(lowest_chunk)
            prompt = _assemble_prompt(compressed_chunks)
            estimated_tokens = prompt_builder.estimate_token_count(prompt)
            logger.warning(f"Truncated 1 lowest-similarity chunk. New estimated tokens: {estimated_tokens}")

    # Sanitize user query string (strip trailing slashes that break string formatting)
    query = query.strip().rstrip('\\').rstrip('/').strip()

    # 8. Local LLM streaming — keep_alive prevents model unloading between requests
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": True,
        "keep_alive": "30m",
        "options": {
            "num_ctx": NUM_CTX,
            "temperature": 0.1,
            "repeat_penalty": 1.15,
            "num_thread": 4
        }
    }

    full_text = ""
    total_tokens = 0
    token_buffer = ""
    
    try:
        response = requests.post(settings.OLLAMA_URL, json=payload, stream=True, timeout=120)
        if response.status_code != 200:
            err_msg = response.text[:300]
            logger.warning(f"Ollama returned HTTP {response.status_code}: {err_msg}")
            # Retry with fallback compressed prompt and lower context window (1024) to avoid runner crashes
            for attempt in range(3):
                wait = 2 ** attempt  # 1s, 2s, 4s
                time.sleep(wait)
                first_c = compressed_chunks[0] if compressed_chunks else {}
                compact_context = (first_c.get('text') or first_c.get('content') or '')[:500]
                retry_payload = {
                    "model": MODEL_NAME,
                    "prompt": f"Question: {query}\n\nRelevant Info: {compact_context}\n\nAnswer in clear Hindi/Hinglish:",
                    "stream": True,
                    "keep_alive": "30m",
                    "options": {
                        "num_ctx": 1024,
                        "temperature": 0.2
                    }
                }
                logger.info(f"Retry attempt {attempt + 1}/3 with compact context payload...")
                response = requests.post(settings.OLLAMA_URL, json=retry_payload, stream=True, timeout=120)
                if response.status_code == 200:
                    break
            
            if response.status_code != 200:
                logger.error(f"Ollama error after retries ({response.status_code}): {response.text[:200]}")
                # Grounded fallback if Ollama runner process crashed under memory pressure
                if compressed_chunks:
                    c = compressed_chunks[0]
                    c_title = c.get('source') or c.get('filename') or c.get('title') or 'Government Guidelines'
                    c_text = c.get('text') or c.get('content') or c.get('page_content') or ''
                    fallback_text = f"**{c_title}**\n\n{c_text[:700]}\n\n[1]"
                else:
                    fallback_text = "Aapka query receive ho gaya hai. Kripya apna prashna thoda short karke poochein."
                full_text = fallback_text
                yield {"type": "token", "data": {"token": fallback_text}}
                return

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode('utf-8'))
                token = data.get("response", "")
                full_text += token
                total_tokens += 1
                token_buffer += token
                
                # Stream in fast word/phrase chunks (>= 6 chars or space/line breaks) for instant TTFT on screen
                if len(token_buffer) >= 6 or any(c in token_buffer for c in ['\n', '.', '!', '?', ';', ' ']):
                    yield {
                        "type": "token",
                        "data": {"token": token_buffer}
                    }
                    token_buffer = ""
                
                if data.get("done", False):
                    break

        # Flush any remaining text buffer
        if token_buffer:
            yield {
                "type": "token",
                "data": {"token": token_buffer}
            }
            token_buffer = ""
    except Exception as e:
        import traceback
        logger.error(f"Ollama inference failed: {e}\n{traceback.format_exc()}")
        if compressed_chunks and not full_text:
            c = compressed_chunks[0]
            c_title = c.get('source') or c.get('filename') or c.get('title') or 'Government Guidelines'
            c_text = c.get('text') or c.get('content') or c.get('page_content') or ''
            fallback_text = f"**{c_title}**\n\n{c_text[:700]}\n\n[1]"
            yield {"type": "token", "data": {"token": fallback_text}}
        else:
            yield {"type": "error", "data": {"message": f"Inference error ({type(e).__name__}): {str(e)}"}}
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
        validated_text = output_validator.validate_and_refine_output(validated_text, context_chunks, language=lang)

        
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

        # Fallback 1: If no explicit inline [1] citations were written in response text, map context_chunks
        if len(citations_used) == 0 and len(context_chunks) > 0:
            for idx, chunk in enumerate(context_chunks, 1):
                citations_used.append({
                    "index": idx,
                    "filename": chunk.get("source") or chunk.get("filename") or "Uploaded Document",
                    "page_number": chunk.get("page_number", 1),
                    "domain": chunk.get("domain", "user_upload"),
                    "collection": chunk.get("collection", "user_docs"),
                    "text_preview": chunk.get("text", "")[:150]
                })

        # Fallback 2: If citations_used is still empty but active_conv_docs exist in session/conversation, map uploaded documents
        if len(citations_used) == 0 and active_conv_docs:
            for idx, doc in enumerate(active_conv_docs, 1):
                citations_used.append({
                    "index": idx,
                    "filename": doc.get("original_filename") or doc.get("filename") or "Uploaded Document",
                    "page_number": 1,
                    "domain": doc.get("domain_hint") or "user_upload",
                    "collection": "user_docs",
                    "text_preview": "Uploaded Document Source"
                })

        # Deduplicate citations by (filename, page_number) while preserving index ordering
        unique_citations = []
        seen_source_pages = set()
        for c in citations_used:
            fn = c.get("filename") or "Document"
            pg = c.get("page_number") or 1
            key = (fn, pg)
            if key not in seen_source_pages:
                seen_source_pages.add(key)
                unique_citations.append(c)
        citations_used = unique_citations
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
