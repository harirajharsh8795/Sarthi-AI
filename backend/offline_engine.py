import socket
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.offline")

class OfflineIntelligenceEngine:
    """
    Validates the local-readiness checklist of system components
    and determines internet connectivity.
    """

    def is_internet_available(self) -> bool:
        """Checks internet connectivity by attempting to resolve a public address."""
        try:
            # Short DNS resolve timeout to prevent latency hangs
            socket.setdefaulttimeout(1.0)
            socket.gethostbyname("dns.google")
            return True
        except Exception:
            return False

    def check_offline_readiness(self) -> dict:
        """
        Runs the local readiness checklist.
        Returns check lists and an Offline Readiness Score (0-100).
        """
        internet_online = self.is_internet_available()
        
        # 1. Model Availability
        model_available = False
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1.0)
            if r.status_code == 200:
                model_available = True
        except Exception:
            pass
            
        # 2. SQLite availability
        sqlite_available = False
        try:
            import session_manager
            conn = session_manager.get_db_connection()
            conn.execute("SELECT 1").fetchone()
            conn.close()
            sqlite_available = True
        except Exception:
            pass
            
        # 3. Embeddings local availability
        embeddings_available = False
        try:
            import services
            # Verify if singleton is loaded or folder exists
            embeddings_available = services.embedding_service is not None
        except Exception:
            pass
            
        # 4. Voice local availability (TTS / STT check)
        voice_available = False
        try:
            import pyttsx3
            # Attempt instantiation test
            engine = pyttsx3.init()
            voice_available = True
            del engine
        except Exception:
            pass

        # Calculate Score out of 100
        # Start at 100, subtract if key components are missing
        score = 100
        
        checklist = {
            "internet_offline": {
                "status": "PASS" if not internet_online else "WARNING",
                "message": "Offline-ready (No active public internet connection detected)" if not internet_online else "Online (Connected to the internet)"
            },
            "model_available": {
                "status": "PASS" if model_available else "FAIL",
                "message": "Local llama3.2:1b Ollama model is responsive" if model_available else "Local Ollama model is offline"
            },
            "sqlite_available": {
                "status": "PASS" if sqlite_available else "FAIL",
                "message": "SQLite database connection is functional" if sqlite_available else "SQLite database is locked or corrupted"
            },
            "embeddings_available": {
                "status": "PASS" if embeddings_available else "FAIL",
                "message": "Sentence transformers embedding model is pre-loaded" if embeddings_available else "Embeddings model failed to load offline"
            },
            "voice_available": {
                "status": "PASS" if voice_available else "WARNING",
                "message": "Local speech synthesis engine initialized" if voice_available else "Pyttsx3 TTS is offline or missing drivers"
            }
        }
        
        # Deduct penalties for FAILS
        if not model_available:
            score -= 30
        if not sqlite_available:
            score -= 30
        if not embeddings_available:
            score -= 20
        if not voice_available:
            score -= 10
            
        return {
            "offline_score": max(0, score),
            "checklist": checklist,
            "internet_online": internet_online
        }

offline_engine = OfflineIntelligenceEngine()
