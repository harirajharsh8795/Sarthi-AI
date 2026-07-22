import os
import logging
from logging.handlers import RotatingFileHandler
from config import settings

# Thread-local request storage to attach Request ID to logs dynamically
import threading
log_context = threading.local()

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(log_context, "request_id", "GLOBAL")
        return True

def setup_logging():
    """Sets up rotated daily/sized logging for stdout and file handlers."""
    import sys
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    os.makedirs(settings.LOGS_DIR, exist_ok=True)
    
    log_format = "[%(asctime)s] [%(levelname)s] [ReqID: %(request_id)s] [%(name)s] [%(threadName)s] %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Clear existing handlers to prevent duplicate logs
    if root_logger.handlers:
        root_logger.handlers.clear()
        
    # Request ID filter
    req_filter = RequestIdFilter()
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(req_filter)
    root_logger.addHandler(console_handler)
    
    # Rotating File Handler
    log_file_path = os.path.join(settings.LOGS_DIR, "saarthi_app.log")
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=settings.LOG_MAX_BYTES,
        backupCount=settings.LOG_BACKUP_COUNT,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.addFilter(req_filter)
    root_logger.addHandler(file_handler)
    
    # Silent noisy libraries
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
    
    logging.info("Rotated structured logger successfully initialized.")

# Run setup
setup_logging()
logger = logging.getLogger("saarthi")
