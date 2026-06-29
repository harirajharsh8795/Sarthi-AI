import os
from pydantic import BaseModel, HttpUrl, ValidationError

class Settings(BaseModel):
    # Paths configuration
    DATA_DIR: str = "./data"
    SQLITE_DIR: str = "./data/sqlite"
    DB_PATH: str = "./data/sqlite/saarthi.db"
    CHROMA_DIR: str = "./data/chroma_db"
    KB_DIR: str = "./data/knowledge_base"
    TEMP_DIR: str = "./data/temp"
    LOGS_DIR: str = "./data/logs"

    # Model configuration
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    LLM_MODEL_NAME: str = "llama3.2:1b"
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

    # OCR and Upload constraints
    MAX_UPLOAD_SIZE: int = 15 * 1024 * 1024  # 15MB
    OCR_LOW_CONFIDENCE_THRESHOLD: float = 50.0

    # Tuning flags
    ENABLE_WAL_MODE: bool = True
    ENABLE_DB_FOREIGN_KEYS: bool = True
    DB_TIMEOUT: float = 30.0

    # Log retention
    LOG_BACKUP_COUNT: int = 5
    LOG_MAX_BYTES: int = 10 * 1024 * 1024  # 10MB

def load_settings() -> Settings:
    """Loads configuration with environment overrides and default values."""
    # Ensure default env variables override
    settings_dict = {
        "DATA_DIR": os.getenv("SAARTHI_DATA_DIR", "./data"),
        "SQLITE_DIR": os.getenv("SAARTHI_SQLITE_DIR", "./data/sqlite"),
        "DB_PATH": os.getenv("SAARTHI_DB_PATH", "./data/sqlite/saarthi.db"),
        "CHROMA_DIR": os.getenv("SAARTHI_CHROMA_DIR", "./data/chroma_db"),
        "KB_DIR": os.getenv("SAARTHI_KB_DIR", "./data/knowledge_base"),
        "TEMP_DIR": os.getenv("SAARTHI_TEMP_DIR", "./data/temp"),
        "LOGS_DIR": os.getenv("SAARTHI_LOGS_DIR", "./data/logs"),
        "OLLAMA_URL": os.getenv("SAARTHI_OLLAMA_URL", "http://localhost:11434/api/generate"),
        "LLM_MODEL_NAME": os.getenv("SAARTHI_LLM_MODEL_NAME", "llama3.2:1b"),
        "EMBEDDING_MODEL_NAME": os.getenv("SAARTHI_EMBEDDING_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"),
        "MAX_UPLOAD_SIZE": int(os.getenv("SAARTHI_MAX_UPLOAD_SIZE", str(15 * 1024 * 1024))),
        "OCR_LOW_CONFIDENCE_THRESHOLD": float(os.getenv("SAARTHI_OCR_LOW_CONFIDENCE_THRESHOLD", "50.0")),
        "ENABLE_WAL_MODE": os.getenv("SAARTHI_ENABLE_WAL_MODE", "True").lower() in ("true", "1", "yes"),
        "ENABLE_DB_FOREIGN_KEYS": os.getenv("SAARTHI_ENABLE_DB_FOREIGN_KEYS", "True").lower() in ("true", "1", "yes"),
        "DB_TIMEOUT": float(os.getenv("SAARTHI_DB_TIMEOUT", "30.0")),
    }
    
    try:
        settings = Settings(**settings_dict)
        
        # 1. Sanity check: Ensure folders are writable
        for folder_path in [settings.DATA_DIR, settings.SQLITE_DIR, settings.CHROMA_DIR, settings.TEMP_DIR, settings.LOGS_DIR]:
            try:
                os.makedirs(folder_path, exist_ok=True)
            except Exception as pe:
                print(f"WARNING: Configuration path {folder_path} is not writable: {pe}")
                
        # 2. Secret checks
        if "key" in settings.OLLAMA_URL.lower():
            print("WARNING: Secret key pattern detected in Ollama connection endpoint URL.")
            
        return settings
    except ValidationError as e:
        print(f"Configuration validation failed: {e}")
        return Settings()

# Singleton configuration instance
settings = load_settings()
