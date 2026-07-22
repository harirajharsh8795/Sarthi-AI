import os
import json
import uuid
import shutil
import tempfile
import logging
import asyncio
import time
import psutil
import whisper
import pyttsx3
import requests
import subprocess
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks, APIRouter, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from logger_config import log_context
import db_manager
import telemetry
import kb_pipeline
import llm_inference
import session_manager
from metrics_manager import metrics_manager
from job_queue import job_queue
from startup_checks import run_environment_checks

from prompt_guard import prompt_guard
from file_security import file_security_validator
from rate_limit import rate_limiter
from audit_service import audit_trail_service
from logger_config import logger

logger = logging.getLogger("saarthi.api")

# Uptime tracker
START_TIME = time.time()

# Conversation Locks dict mapping conversation_id -> asyncio.Task
active_streams = {}
active_streams_lock = asyncio.Lock()

# Custom error structure for user friendly API messages
class SaarthiError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 500):
        self.code = code
        self.message = message
        self.status_code = status_code

# Health check cache
health_cache = None
health_cache_time = 0.0

# Request Models
class SessionRequest(BaseModel):
    display_name: Optional[str] = None

class ConversationCreate(BaseModel):
    session_id: str
    title: Optional[str] = "New Conversation"
    device_id: Optional[str] = None

class ConversationUpdate(BaseModel):
    title: str

class SpeakRequest(BaseModel):
    text: str
    language: str


# System Lifespan for Graceful Shutdowns
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup check validation
    run_environment_checks()
    # Call whisper and DB initialization
    preload_whisper()
    yield
    # Shutdown resource release
    logger.info("Initiating graceful shutdown sequence...")
    # 1. Cancel active streams
    async with active_streams_lock:
        for conv_id, task in list(active_streams.items()):
            if not task.done():
                logger.info(f"Cancelling active stream task for {conv_id} during shutdown...")
                task.cancel()
    # 2. Release job queue threads
    job_queue.shutdown()
    # 3. Close SQLite connections pool
    db_manager.db_pool.close_all()
    # 4. Release Chroma client
    import services
    services.chroma_manager.close()
    # 5. Flush temp directory
    if os.path.exists(settings.TEMP_DIR):
        try:
            shutil.rmtree(settings.TEMP_DIR)
            logger.info("Flushed temporary directory.")
        except Exception as e:
            logger.error(f"Error flushing temp dir: {e}")
            
    logger.info("Graceful shutdown complete.")


app = FastAPI(
    title="Saarthi RAG API", 
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom request timing and ID middleware
@app.middleware("http")
async def add_request_id_and_timing(request: Request, call_next):
    req_id = request.headers.get("X-Request-ID", f"req_{uuid.uuid4().hex[:8]}")
    log_context.request_id = req_id
    
    start_time = time.perf_counter()
    
    # Check conversation locks for stream queries
    if request.url.path.endswith("/api/stream") or request.url.path.endswith("/api/v1/stream"):
        conv_id = request.query_params.get("conversation_id", "default_conv")
        async with active_streams_lock:
            if conv_id in active_streams:
                old_task = active_streams[conv_id]
                if not old_task.done():
                    logger.info(f"Cancelling running task for conversation {conv_id} due to new stream request")
                    old_task.cancel()
                    try:
                        await old_task
                    except asyncio.CancelledError:
                        pass
            active_streams[conv_id] = asyncio.current_task()
            
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    
    # Inject headers
    response.headers["X-Request-ID"] = req_id
    response.headers["X-Response-Time"] = f"{duration * 1000.0:.2f}ms"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    logger.info(f"{request.method} {request.url.path} completed in {duration * 1000.0:.2f}ms with status {response.status_code}")
    return response

# Custom exceptions formatting
@app.exception_handler(SaarthiError)
async def saarthi_exception_handler(request: Request, exc: SaarthiError):
    req_id = getattr(log_context, "request_id", "GLOBAL")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": exc.code,
            "message": exc.message,
            "request_id": req_id
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    req_id = getattr(log_context, "request_id", "GLOBAL")
    logger.exception(f"Unhandled exception caught on request {req_id}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "SAARTHI_INTERNAL_ERROR",
            "message": "An unexpected error occurred. Please try again.",
            "request_id": req_id
        }
    )


# Versioned router
v1_router = APIRouter(prefix="/api/v1")

whisper_model = None

def get_ffmpeg_path():
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    user_profile = os.environ.get("USERPROFILE", "")
    winget_link = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Links", "ffmpeg.exe")
    if os.path.exists(winget_link):
        return winget_link
    packages_dir = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Packages")
    if os.path.exists(packages_dir):
        for root, dirs, files in os.walk(packages_dir):
            if "ffmpeg.exe" in files:
                return os.path.join(root, "ffmpeg.exe")
    return None

# Load Whisper in a startup event hook
@app.on_event("startup")
def preload_whisper():
    global whisper_model
    # Expose ffmpeg directory to system PATH
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path and ffmpeg_path != "ffmpeg":
        ffmpeg_dir = os.path.dirname(os.path.abspath(ffmpeg_path))
        if ffmpeg_dir not in os.environ["PATH"].split(os.pathsep):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
            logger.info(f"Added ffmpeg directory to PATH: {ffmpeg_dir}")
            
    logger.info("Pre-loading Whisper tiny model...")
    try:
        whisper_model = whisper.load_model("tiny")
        logger.info("Whisper loaded OK")
    except Exception as e:
        logger.error(f"WARNING: Whisper failed: {e}")
        whisper_model = None
        
    try:
        session_manager.init_session_db()
        logger.debug("Database initialized")
    except Exception as e:
        logger.error(f"Error initializing session DB: {e}")

    # Preload LLM and Embedding models asynchronously to not block startup checks
    def warmup_models_task():
        # 1. Warm up Ollama LLM
        try:
            from model_manager import model_lifecycle_manager
            model_lifecycle_manager.warmup_model()
        except Exception as e:
            logger.error(f"Error pre-warming LLM: {e}")
            
        # 2. Warm up SentenceTransformer Embedding Model
        try:
            import kb_pipeline
            logger.info("Pre-warming embedding model...")
            kb_pipeline.get_embedding_model()
            logger.info("Embedding model pre-warmed successfully.")
        except Exception as e:
            logger.error(f"Error pre-warming embedding model: {e}")

    import threading
    threading.Thread(target=warmup_models_task, daemon=True).start()


# v1 ENDPOINTS

@v1_router.post("/session")
def create_session(request: SessionRequest = SessionRequest()):
    try:
        new_id = f"session_{uuid.uuid4().hex[:8]}"
        session_data = session_manager.get_or_create_session(new_id, request.display_name)
        return {
            "session_id": session_data["session_id"],
            "created_at": session_data["created_at"]
        }
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to create session.")

@v1_router.post("/upload")
def upload_document(
    request: Request,
    file: UploadFile = File(...), 
    session_id: str = Form(...), 
    conversation_id: Optional[str] = Form(None)
):
    start_time = time.perf_counter()
    req_id = getattr(log_context, "request_id", "GLOBAL")
    
    # 1. Rate Limiting Check
    if rate_limiter.is_rate_limited(request, "upload"):
        audit_trail_service.log_event("rate_limit_exceeded", "Upload limit reached", "REJECTED", "WARNING", req_id)
        return JSONResponse(status_code=429, content={"message": "Too many requests. Please try again later."})
    
    # 2. Validation checks
    ext = os.path.splitext(file.filename)[1].lower()
    valid_extensions = {".pdf", ".docx", ".jpg", ".jpeg", ".png", ".webp", ".txt"}
    if ext not in valid_extensions:
        raise SaarthiError("SAARTHI_INVALID_FILE", f"Unsupported file extension: {ext}", 400)

    # Temporary copy to run hash checking
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(suffix=ext, dir=settings.TEMP_DIR, delete=False)
    temp_file_path = temp_file.name
    
    try:
        shutil.copyfileobj(file.file, temp_file)
        temp_file.close()
        
        # 3. Magic Bytes & Extensions Security validation
        val = file_security_validator.validate_file_safety(temp_file_path, file.filename)
        if not val["safe"]:
            os.remove(temp_file_path)
            audit_trail_service.log_event("malicious_upload_blocked", f"File: {file.filename}, Reason: {val['reason']}", "BLOCKED", "HIGH", req_id)
            raise SaarthiError("SAARTHI_SECURITY_BLOCK", val["reason"], 400)
            
        # Log successful upload in audit
        audit_trail_service.log_event("document_upload_success", f"File: {file.filename}, Session: {session_id}", "SUCCESS", "INFO", req_id)

        # Check upload size limit
        file_size = os.path.getsize(temp_file_path)
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise SaarthiError("SAARTHI_FILE_TOO_LARGE", "File size exceeds 15MB limit.", 400)
            
        # Duplicate detection (MD5 hash)
        file_hash = kb_pipeline.calculate_file_hash(temp_file_path)
        existing_docs = session_manager.get_session_documents(session_id, conversation_id=conversation_id)
        for d in existing_docs:
            if d.get("file_hash") == file_hash:
                logger.info(f"Duplicate upload detected: {file.filename}. Reusing document {d['id']}")
                # Clean temp copy
                os.remove(temp_file_path)
                return {
                    "session_id": session_id,
                    "document_id": d["id"],
                    "original_filename": file.filename,
                    "status": d["status"],
                    "page_count": d["page_count"],
                    "chunk_count": d["chunk_count"],
                    "ocr_used": d["ocr_used"],
                    "ocr_confidence": d["ocr_confidence"],
                    "ocr_low_quality_warning": d["ocr_low_quality_warning"],
                    "message": "Duplicate file detected. Reusing existing vector index."
                }
                
        # Register new document record in SQLite
        document_id = f"doc_{uuid.uuid4().hex}"
        ocr_used = ext in {".jpg", ".jpeg", ".png", ".webp"}
        
        session_manager.create_document_record(
            document_id=document_id,
            session_id=session_id,
            original_filename=file.filename,
            file_type=ext,
            domain_hint=None,
            ocr_used=ocr_used,
            status="pending",
            conversation_id=conversation_id,
            file_hash=file_hash
        )
        
        # Register Background Job Ingestion
        job_id = job_queue.create_job(document_id, conversation_id)
        
        # Schedule task thread execution
        job_queue.submit_task(
            kb_pipeline.ingest_user_document_task,
            job_id,
            temp_file_path,
            file.filename,
            session_id,
            None,
            conversation_id,
            file_hash,
            document_id
        )
        
        duration = time.perf_counter() - start_time
        metrics_manager.record("upload_time", duration)
        
        return {
            "session_id": session_id,
            "document_id": document_id,
            "job_id": job_id,
            "original_filename": file.filename,
            "status": "pending",
            "message": "Ingestion task queued successfully."
        }
        
    except SaarthiError as se:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise se
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        logger.error(f"Upload task submission error: {e}")
        raise SaarthiError("SAARTHI_UPLOAD_FAILED", "Failed to schedule upload task.")

@v1_router.get("/uploads/{job_id}")
def get_job_status(job_id: str):
    job = job_queue.get_job(job_id)
    if not job:
        raise SaarthiError("SAARTHI_JOB_NOT_FOUND", "Background job not found.", 404)
    return job

@v1_router.get("/stream")
def generate_stream(
    request: Request,
    query: str, 
    session_id: str, 
    conversation_id: Optional[str] = None, 
    response_language: Optional[str] = None
):
    req_id = getattr(log_context, "request_id", "GLOBAL")
    
    # 1. Rate Limiting Check
    if rate_limiter.is_rate_limited(request, "stream"):
        audit_trail_service.log_event("rate_limit_exceeded", "Stream limit reached", "REJECTED", "WARNING", req_id, conversation_id)
        return JSONResponse(status_code=429, content={"message": "Too many requests. Please try again later."})
        
    # 2. Prompt Guard (Injection/Jailbreak protection checks)
    guard = prompt_guard.scan_query(query)
    if guard["blocked"]:
        audit_trail_service.log_event(
            event_type="prompt_injection_blocked",
            details=f"Query: {query[:100]}, Rule: {guard['rule_triggered']}",
            result="BLOCKED",
            severity="HIGH",
            request_id=req_id,
            conversation_id=conversation_id
        )
        return JSONResponse(status_code=400, content={
            "blocked": True,
            "reason": guard["reason"],
            "risk_level": guard["risk_level"],
            "rule_triggered": guard["rule_triggered"],
            "request_id": req_id
        })
        
    # Log valid query trigger
    audit_trail_service.log_event("query_started", f"Query: {query[:80]}", "SUCCESS", "INFO", req_id, conversation_id)

    async def event_generator():
        loop = asyncio.get_event_loop()
        try:
            # We call the generator inside executor thread to avoid blocking loop
            # llm_inference.generate_answer_stream is synchronous generator
            gen = llm_inference.generate_answer_stream(query, session_id, response_language, conversation_id)
            
            last_heartbeat = time.time()
            
            while True:
                # Run next generator yield in thread pool
                data = await loop.run_in_executor(None, next, gen, None)
                if data is None:
                    break
                yield f"data: {json.dumps(data)}\n\n"
                
                # Heartbeat injection
                now = time.time()
                if now - last_heartbeat > 15:
                    yield ": keep-alive\n\n"
                    last_heartbeat = now
                    
            yield "data: [DONE]\n\n"
        except StopIteration:
            yield "data: [DONE]\n\n"
        except asyncio.CancelledError:
            logger.info("Stream cancelled by client disconnect or lock release.")
            # Clear lock registration
            if conversation_id and active_streams.get(conversation_id) == asyncio.current_task():
                del active_streams[conversation_id]
        except Exception as e:
            import traceback
            logger.error(f"Stream generation error: {e}\n{traceback.format_exc()}")
            error_msg = f"Something went wrong while generating the response.\n\nRequest ID: {req_id}"
            yield f"data: {json.dumps({'type': 'error', 'data': {'message': error_msg}})}\n\n"

    return StreamingResponse(
        event_generator(), 
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@v1_router.get("/history")
def get_session_history(session_id: str, conversation_id: Optional[str] = None):
    try:
        documents = session_manager.list_session_documents(session_id, conversation_id)
        return {
            "session_id": session_id,
            "documents": documents
        }
    except Exception as e:
        logger.error(f"Error fetching history: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to retrieve documents history.")

@v1_router.get("/telemetry")
def get_telemetry():
    try:
        records = telemetry.get_recent_telemetry(n=20)
        total_queries = len(records)
        
        total_tokens_per_second = 0.0
        total_generation_time_ms = 0.0
        queries_with_context = 0
        queries_skipped_llm = 0
        
        for r in records:
            tps = r.get("tokens_per_second")
            if tps is not None:
                total_tokens_per_second += float(tps)
            gt = r.get("generation_time_ms")
            if gt is not None:
                total_generation_time_ms += float(gt)
            if r.get("has_context"):
                queries_with_context += 1
            if r.get("skipped_llm"):
                queries_skipped_llm += 1
                
        avg_tokens_per_second = (total_tokens_per_second / total_queries) if total_queries > 0 else 0.0
        avg_generation_time_ms = (total_generation_time_ms / total_queries) if total_queries > 0 else 0.0
        
        return {
            "records": records,
            "summary": {
                "avg_tokens_per_second": round(avg_tokens_per_second, 2),
                "avg_generation_time_ms": round(avg_generation_time_ms, 2),
                "total_queries": total_queries,
                "queries_with_context": queries_with_context,
                "queries_skipped_llm": queries_skipped_llm
            }
        }
    except Exception as e:
        logger.error(f"Error fetching telemetry: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to retrieve telemetry logs.")

@v1_router.post("/voice/transcribe")
async def transcribe_audio(audio: UploadFile = File(...), lang: Optional[str] = Form(None)):
    if whisper_model is None:
        return JSONResponse({"success": False, "error": "Voice input is not available. Please type your question instead."}, status_code=200)
    
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(suffix=".webm", dir=settings.TEMP_DIR, delete=False)
    temp_file_path = temp_file.name
    
    wav_file_path = None
    try:
        shutil.copyfileobj(audio.file, temp_file)
        temp_file.close()
        
        transcribe_target = temp_file_path
        ffmpeg_path = get_ffmpeg_path()
        
        if ffmpeg_path:
            wav_file_path = temp_file_path + ".wav"
            try:
                cmd = [ffmpeg_path, "-y", "-i", temp_file_path, "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav_file_path]
                import subprocess
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                transcribe_target = wav_file_path
            except Exception as e:
                logger.error(f"ffmpeg conversion failed: {e}")
                
        loop = asyncio.get_event_loop()
        def run_whisper():
            return whisper_model.transcribe(
                transcribe_target,
                fp16=False,
                language=lang if lang in ["hi", "en"] else None
            )
            
        result = await loop.run_in_executor(None, run_whisper)
        
        return {
            "transcript": result.get("text", "").strip(),
            "detected_language": result.get("language", "unknown")
        }
    except Exception as e:
        logger.error(f"Audio transcription failed: {e}")
        raise SaarthiError("SAARTHI_STT_FAILED", "Failed to transcribe audio.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if wav_file_path and os.path.exists(wav_file_path):
            os.remove(wav_file_path)

@v1_router.post("/voice/speak")
async def speak_text(request: SpeakRequest, background_tasks: BackgroundTasks):
    os.makedirs(settings.TEMP_DIR, exist_ok=True)
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", dir=settings.TEMP_DIR, delete=False)
    temp_file_path = temp_file.name
    temp_file.close()
    
    try:
        loop = asyncio.get_event_loop()
        def run_pyttsx3():
            engine = pyttsx3.init()
            try:
                engine.setProperty('rate', 150)
                if request.language == "Hindi":
                    voices = engine.getProperty('voices')
                    hindi_voice = None
                    for voice in voices:
                        name_str = str(voice.name).lower()
                        id_str = str(voice.id).lower()
                        lang_str = str(getattr(voice, 'languages', [])).lower()
                        if "hindi" in name_str or "hi_in" in id_str or "hindi" in lang_str:
                            hindi_voice = voice.id
                            break
                    if hindi_voice:
                        engine.setProperty('voice', hindi_voice)
                engine.save_to_file(request.text, temp_file_path)
                engine.runAndWait()
            finally:
                del engine

        await loop.run_in_executor(None, run_pyttsx3)
        
        if not os.path.exists(temp_file_path) or os.path.getsize(temp_file_path) == 0:
            raise SaarthiError("SAARTHI_TTS_FAILED", "Pyttsx3 generated file is empty.", 500)
            
        background_tasks.add_task(lambda path: os.path.exists(path) and os.remove(path), temp_file_path)
        return FileResponse(temp_file_path, media_type="audio/wav")
    except Exception as e:
        logger.error(f"Speak synthesis failed: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise SaarthiError("SAARTHI_TTS_FAILED", "Failed to synthesize speech.")

@v1_router.post("/conversations")
def create_new_conversation(req: ConversationCreate):
    try:
        conversation_id = f"conv_{uuid.uuid4().hex[:8]}"
        session_manager.create_conversation(conversation_id, req.session_id, req.title, getattr(req, 'device_id', None))
        return {"conversation_id": conversation_id}
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to create conversation.")

@v1_router.get("/conversations/all")
def get_all_conversations(device_id: str):
    try:
        conversations = session_manager.list_all_conversations(device_id)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error fetching all conversations: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to retrieve conversations.")

@v1_router.get("/conversations")
def get_conversations(session_id: str):
    try:
        conversations = session_manager.list_conversations(session_id)
        return {"conversations": conversations}
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to retrieve conversations.")

@v1_router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: str):
    try:
        messages = session_manager.get_conversation_messages(conversation_id)
        return {"messages": messages}
    except Exception as e:
        logger.error(f"Error fetching messages: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to retrieve messages.")

@v1_router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, session_id: str):
    try:
        doc_ids = session_manager.delete_conversation(conversation_id, session_id)
        cleaned_count = 0
        for doc_id in doc_ids:
            try:
                kb_pipeline.delete_document_and_chunks(doc_id, session_id)
                cleaned_count += 1
            except Exception as vector_err:
                logger.error(f"Failed to delete vector chunks for document {doc_id}: {vector_err}")
                
        return {
            "success": True, 
            "message": "Conversation deleted successfully", 
            "documents_cleaned": cleaned_count
        }
    except Exception as e:
        logger.error(f"Error deleting conversation: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to delete conversation.")

@v1_router.put("/conversations/{conversation_id}")
def update_conversation(conversation_id: str, req: ConversationUpdate):
    try:
        conn = session_manager.get_db_connection()
        cursor = conn.cursor()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (req.title, now_str, conversation_id)
        )
        conn.commit()
        conn.close()
        return {"success": True, "title": req.title}
    except Exception as e:
        logger.error(f"Error renaming conversation: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to rename conversation.")

@v1_router.delete("/conversations/{conversation_id}/messages/{message_id}")
def delete_messages_from(conversation_id: str, message_id: str):
    try:
        deleted_count = session_manager.delete_messages_after(conversation_id, message_id)
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"Error deleting messages: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to edit messages history.")

@v1_router.get("/search/messages")
def search_messages(session_id: str, q: str):
    try:
        results = session_manager.search_messages(session_id, q)
        return {"results": results}
    except Exception as e:
        logger.error(f"Error searching messages: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to search messages.")

@v1_router.delete("/document/{document_id}")
def delete_document(document_id: str, session_id: str):
    try:
        kb_pipeline.delete_document_and_chunks(document_id, session_id)
        return {"success": True, "message": "Document deleted"}
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to delete document.")

@v1_router.get("/health")
def health_check():
    global health_cache, health_cache_time
    now = time.time()
    
    # 5 seconds health caching
    if health_cache is not None and now - health_cache_time < 5.0:
        return health_cache
        
    try:
        # Check Ollama status
        ollama_status = "offline"
        try:
            tags_url = settings.OLLAMA_URL.replace("/api/generate", "/api/tags")
            r = requests.get(tags_url, timeout=1.5)
            if r.status_code == 200:
                ollama_status = "ok"
        except Exception:
            pass
            
        # SQLite status check
        sqlite_status = "ok"
        try:
            conn = session_manager.get_db_connection()
            conn.execute("SELECT 1").fetchone()
            conn.close()
        except Exception:
            sqlite_status = "error"
            
        # ChromaDB check
        chroma_status = "ok"
        kb_chunks = 0
        try:
            import services
            collection = services.chroma_manager.get_collection("knowledge_base")
            kb_chunks = collection.count()
        except Exception:
            chroma_status = "error"
            
        # System Resource timings
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        health_cache = {
            "status": "healthy",
            "uptime_seconds": int(time.time() - START_TIME),
            "ollama_status": ollama_status,
            "sqlite_status": sqlite_status,
            "chroma_status": chroma_status,
            "kb_chunks": kb_chunks,
            "memory_usage_pct": mem.percent,
            "cpu_usage_pct": psutil.cpu_percent(),
            "disk_usage_pct": disk.percent,
            "metrics": metrics_manager.get_all_summaries()
        }
        health_cache_time = now
        return health_cache
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise SaarthiError("SAARTHI_HEALTH_FAILED", "Failed to calculate health stats.")


@v1_router.get("/system/health")
def get_system_health():
    from edge_score import edge_performance_scorecard
    return edge_performance_scorecard.calculate_readiness_score()

@v1_router.get("/system/resources")
def get_system_resources():
    from resource_monitor import resource_monitor
    snapshot = resource_monitor.collect_snapshot()
    history = resource_monitor.get_timeline_data()
    return {
        "current_snapshot": snapshot,
        "timeline_history": history
    }

@v1_router.get("/system/cache")
def get_system_cache():
    from cache_manager import cache_manager
    return cache_manager.get_global_metrics()

@v1_router.get("/system/performance")
def get_system_performance():
    from metrics_manager import metrics_manager
    return metrics_manager.get_all_summaries()

@v1_router.get("/system/deployment")
def get_system_deployment():
    from deployment_validator import deployment_validator
    return deployment_validator.validate_deployment()

@v1_router.get("/system/diagnostics")
def get_system_diagnostics():
    from diagnostics import system_diagnostics
    return system_diagnostics.diagnose_system()

@v1_router.get("/observability")
def get_system_observability():
    from observability_service import observability_service
    return observability_service.get_observability_metrics()


@v1_router.get("/security/status")
def get_security_status():
    from secret_scanner import secret_scanner
    return secret_scanner.scan_project_secrets()

@v1_router.get("/security/audit")
def get_security_audit():
    return audit_trail_service.list_audit_logs()

@v1_router.get("/security/compliance")
def get_security_compliance():
    from compliance_service import compliance_service
    return compliance_service.compile_compliance_metrics()

@v1_router.get("/security/trust")
def get_security_trust():
    from edge_score import edge_performance_scorecard
    return edge_performance_scorecard.calculate_readiness_score()

@v1_router.get("/security/production")
def get_security_production():
    from production_validator import production_validator
    return production_validator.run_production_checks()


@v1_router.get("/telemetry/{inference_id}/inspect")
def inspect_telemetry(inference_id: str):
    """
    Retrieves full Stage 2 cognitive execution telemetry metadata block
    for a specific query run instance. Used by the Retrieval Inspector.
    """
    try:
        record = telemetry.get_telemetry_by_id(inference_id)
        if not record:
            raise SaarthiError("SAARTHI_INSPECT_NOT_FOUND", "Inference trace ID not found.", 404)
        return record
    except SaarthiError as se:
        raise se
    except Exception as e:
        logger.error(f"Error fetching inspection details: {e}")
        raise SaarthiError("SAARTHI_DB_ERROR", "Failed to retrieve inspection trace.")


# Include routers and register root aliases for backward compatibility
app.include_router(v1_router)

# ALIAS REGISTER DIRECT MAP
@app.post("/api/session")
def alias_create_session(request: SessionRequest = SessionRequest()):
    return create_session(request)

@app.post("/api/upload")
def alias_upload_document(request: Request, file: UploadFile = File(...), session_id: str = Form(...), conversation_id: Optional[str] = Form(None)):
    return upload_document(request, file, session_id, conversation_id)

@app.get("/api/uploads/{job_id}")
def alias_get_job_status(job_id: str):
    return get_job_status(job_id)

@app.get("/api/stream")
def alias_generate_stream(request: Request, query: str, session_id: str, conversation_id: Optional[str] = None, response_language: Optional[str] = None):
    return generate_stream(request, query, session_id, conversation_id, response_language)

@app.get("/api/history")
def alias_get_session_history(session_id: str, conversation_id: Optional[str] = None):
    return get_session_history(session_id, conversation_id)

@app.get("/api/telemetry")
def alias_get_telemetry():
    return get_telemetry()

@app.post("/api/voice/transcribe")
async def alias_transcribe_audio(audio: UploadFile = File(...), lang: Optional[str] = Form(None)):
    return await transcribe_audio(audio, lang)

@app.post("/api/voice/speak")
async def alias_speak_text(request: SpeakRequest, background_tasks: BackgroundTasks):
    return await speak_text(request, background_tasks)

@app.post("/api/conversations")
def alias_create_new_conversation(req: ConversationCreate):
    return create_new_conversation(req)

@app.get("/api/conversations/all")
def alias_get_all_conversations(device_id: str):
    return get_all_conversations(device_id)

@app.get("/api/conversations")
def alias_get_conversations(session_id: str):
    return get_conversations(session_id)

@app.get("/api/conversations/{conversation_id}/messages")
def alias_get_conversation_messages(conversation_id: str):
    return get_conversation_messages(conversation_id)

@app.delete("/api/conversations/{conversation_id}")
def alias_delete_conversation(conversation_id: str, session_id: str):
    return delete_conversation(conversation_id, session_id)

@app.put("/api/conversations/{conversation_id}")
def alias_update_conversation(conversation_id: str, req: ConversationUpdate):
    return update_conversation(conversation_id, req)

@app.delete("/api/conversations/{conversation_id}/messages/{message_id}")
def alias_delete_messages_from(conversation_id: str, message_id: str):
    return delete_messages_from(conversation_id, message_id)

@app.get("/api/search/messages")
def alias_search_messages(session_id: str, q: str):
    return search_messages(session_id, q)

@app.delete("/api/document/{document_id}")
def alias_delete_document(document_id: str, session_id: str):
    return delete_document(document_id, session_id)

@app.get("/api/health")
def alias_health_check():
    return health_check()

@app.get("/api/telemetry/{inference_id}/inspect")
def alias_inspect_telemetry(inference_id: str):
    return inspect_telemetry(inference_id)

@app.get("/api/system/health")
def alias_get_system_health():
    return get_system_health()

@app.get("/api/system/resources")
def alias_get_system_resources():
    return get_system_resources()

@app.get("/api/system/cache")
def alias_get_system_cache():
    return get_system_cache()

@app.get("/api/system/performance")
def alias_get_system_performance():
    return get_system_performance()

@app.get("/api/system/deployment")
def alias_get_system_deployment():
    return get_system_deployment()

@app.get("/api/system/diagnostics")
def alias_get_system_diagnostics():
    return get_system_diagnostics()

@app.get("/api/observability")
def alias_get_system_observability():
    return get_system_observability()

@app.get("/api/security/status")
def alias_get_security_status():
    return get_security_status()

@app.get("/api/security/audit")
def alias_get_security_audit():
    return get_security_audit()

@app.get("/api/security/compliance")
def alias_get_security_compliance():
    return get_security_compliance()

@app.get("/api/security/trust")
def alias_get_security_trust():
    return get_security_trust()

@app.get("/api/security/production")
def alias_get_security_production():
    return get_security_production()


# 4. Static Single-Page App Mounting Fallback
dist_dir = "./frontend/dist"
if os.path.exists(dist_dir):
    assets_dir = os.path.join(dist_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        
    @app.get("/{fallback_path:path}")
    def serve_frontend(fallback_path: str):
        index_file = os.path.join(dist_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"message": "Frontend build files found but index.html is missing."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

