import os
import shutil
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.startup")

def run_environment_checks() -> bool:
    """
    Verifies that system folders are present and writable, Tesseract binary is located,
    and Ollama service is reachable.
    Returns True if system is healthy, otherwise returns False or raises warnings.
    """
    logger.info("Executing system validation startup checks...")
    
    # 1. Validate storage directories are writable
    required_dirs = [
        settings.DATA_DIR,
        settings.SQLITE_DIR,
        settings.CHROMA_DIR,
        settings.KB_DIR,
        settings.TEMP_DIR,
        settings.LOGS_DIR
    ]
    
    for directory in required_dirs:
        try:
            os.makedirs(directory, exist_ok=True)
            # Write test file to verify permissions
            test_file = os.path.join(directory, ".write_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            logger.critical(f"Directory check failed: {directory} is not writable. Error: {e}")
            return False

    # 2. Check Tesseract OCR executable
    import pytesseract
    tesseract_found = False
    try:
        tess_cmd = pytesseract.pytesseract.tesseract_cmd
        if tess_cmd and os.path.exists(tess_cmd):
            tesseract_found = True
        elif shutil.which("tesseract"):
            tesseract_found = True
    except Exception:
        pass
        
    if not tesseract_found:
        logger.warning(
            "Tesseract OCR binary not found on PATH or configured directories. "
            "OCR capability on images will fail."
        )

    # 3. Check Ollama tags and models configuration
    ollama_ready = False
    urls_to_try = [settings.OLLAMA_URL]
    # If the default contains localhost, try 127.0.0.1 (common Windows ipv6/ipv4 resolution fallback)
    if "localhost" in settings.OLLAMA_URL:
        urls_to_try.append(settings.OLLAMA_URL.replace("localhost", "127.0.0.1"))
    # If the default contains localhost/127.0.0.1, also try the Docker gateway 172.17.0.1 (common for Jetson Orin host)
    if "localhost" in settings.OLLAMA_URL or "127.0.0.1" in settings.OLLAMA_URL:
        urls_to_try.append(settings.OLLAMA_URL.replace("localhost", "172.17.0.1").replace("127.0.0.1", "172.17.0.1"))
        
    for url in urls_to_try:
        try:
            base_url = url.replace("/api/generate", "")
            r = requests.get(f"{base_url}/api/tags", timeout=2)
            if r.status_code == 200:
                ollama_ready = True
                if url != settings.OLLAMA_URL:
                    logger.info(f"Auto-detected Ollama host at Docker gateway: {url}")
                    settings.OLLAMA_URL = url
                
                models = [m["name"] for m in r.json().get("models", [])]
                if settings.LLM_MODEL_NAME not in models and f"{settings.LLM_MODEL_NAME}:latest" not in models:
                    logger.warning(
                        f"Ollama is running, but model '{settings.LLM_MODEL_NAME}' was not found. "
                        "Inference query pipeline may fail. Run 'ollama pull llama3.2:1b'."
                    )
                else:
                    logger.info(f"Ollama connected. Target model '{settings.LLM_MODEL_NAME}' is pulled and ready.")
                break
        except Exception:
            continue
            
    if not ollama_ready:
        logger.warning(
            f"Ollama service connection failed at {settings.OLLAMA_URL}. "
            "Please ensure Ollama server is running. System will start in DEGRADED mode."
        )

    # 4. Check Voice dependencies (Whisper and pyttsx3)
    voice_ok = True
    try:
        import whisper
        import pyttsx3
        # Attempt minimal validation of pyttsx3 initialization
        engine = pyttsx3.init()
        del engine
        logger.info("Voice dependencies (Whisper, pyttsx3) are installed and initialized successfully.")
    except Exception as e:
        voice_ok = False
        logger.warning(
            f"Voice/Speech engine initialization failed: {e}. "
            "Voice input/output features might be unavailable or degraded."
        )

    # 5. Check FFmpeg binary (critical for audio conversion)
    ffmpeg_found = False
    if shutil.which("ffmpeg"):
        ffmpeg_found = True
    else:
        # Check Windows-specific winget paths
        user_profile = os.environ.get("USERPROFILE", "")
        winget_link = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Links", "ffmpeg.exe")
        if os.path.exists(winget_link):
            ffmpeg_found = True
        else:
            packages_dir = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Packages")
            if os.path.exists(packages_dir):
                for root, dirs, files in os.walk(packages_dir):
                    if "ffmpeg.exe" in files:
                        ffmpeg_found = True
                        break
                        
    if not ffmpeg_found:
        logger.warning(
            "FFmpeg executable not found on PATH. "
            "Audio conversion for Whisper voice transcription will fail."
        )
    else:
        logger.info("FFmpeg executable verified on PATH.")

    logger.info("Startup validation checks completed.")
    return True
