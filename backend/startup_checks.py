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
    try:
        # Infer Ollama URL base
        base_url = settings.OLLAMA_URL.replace("/api/generate", "")
        r = requests.get(f"{base_url}/api/tags", timeout=3)
        if r.status_code == 200:
            ollama_ready = True
            models = [m["name"] for m in r.json().get("models", [])]
            if settings.LLM_MODEL_NAME not in models and f"{settings.LLM_MODEL_NAME}:latest" not in models:
                logger.warning(
                    f"Ollama is running, but model '{settings.LLM_MODEL_NAME}' was not found. "
                    "Inference query pipeline may fail. Run 'ollama pull llama3.2:1b'."
                )
            else:
                logger.info(f"Ollama connected. Target model '{settings.LLM_MODEL_NAME}' is pulled and ready.")
    except Exception as e:
        logger.warning(
            f"Ollama service connection failed at {settings.OLLAMA_URL}. "
            "Please ensure Ollama server is running locally. System will start in DEGRADED mode."
        )

    logger.info("Startup validation checks completed.")
    return True
