import time
import requests
import logging
from config import settings

logger = logging.getLogger("saarthi.models")

class ModelLifecycleManager:
    """
    Manages loading, pre-warming, idle timeouts, and graceful unloads
    of the local llama3.2:1b model running on Ollama.
    """
    
    def __init__(self):
        self.model_name = settings.LLM_MODEL_NAME
        self.warmup_duration_sec = 0.0
        self.model_state = "cold"  # cold, warming, warm, unloaded
        self.last_used_timestamp = time.time()
        self.idle_timeout_sec = 600.0  # 10 minutes idle timeout

    def pull_model_if_missing(self) -> bool:
        """Pulls the model from the Ollama library if not present locally."""
        try:
            # Check local tags first
            tags_url = settings.OLLAMA_URL.replace("/api/generate", "/api/tags")
            r = requests.get(tags_url, timeout=1.5)
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                # Match tags (e.g. llama3.2:1b or llama3.2:1b-instruct)
                if any(self.model_name in m or m in self.model_name for m in models):
                    return True
                    
            logger.warning(f"Model {self.model_name} is missing. Initiating pull...")
            # Trigger asynchronous pull
            pull_url = settings.OLLAMA_URL.replace("/api/generate", "/api/pull")
            requests.post(
                pull_url, 
                json={"name": self.model_name, "stream": False},
                timeout=180
            )
            return True
        except Exception as e:
            logger.error(f"Failed to verify or pull model: {e}")
            return False

    def warmup_model(self) -> bool:
        """Warmups / preloads the model into memory with a dummy query."""
        if self.model_state == "warm":
            return True
            
        logger.info(f"Pre-warming model '{self.model_name}'...")
        self.model_state = "warming"
        start = time.perf_counter()
        
        try:
            # Simple short instruction to load model weights
            r = requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": self.model_name,
                    "prompt": "ping",
                    "stream": False
                },
                timeout=30
            )
            if r.status_code == 200:
                self.warmup_duration_sec = time.perf_counter() - start
                self.model_state = "warm"
                self.last_used_timestamp = time.time()
                logger.info(f"Model warmed up successfully in {self.warmup_duration_sec:.2f} seconds.")
                return True
        except Exception as e:
            logger.error(f"Warmup query failed: {e}")
            
        self.model_state = "cold"
        return False

    def update_usage_timestamp(self):
        self.last_used_timestamp = time.time()
        if self.model_state != "warm":
            self.model_state = "warm"

    def check_idle_unload(self):
        """Unloads model from RAM if idle threshold is crossed."""
        if self.model_state != "warm":
            return
            
        now = time.time()
        if now - self.last_used_timestamp > self.idle_timeout_sec:
            logger.info(f"Model idle timeout crossed ({self.idle_timeout_sec}s). Unloading from RAM...")
            self.unload_model()

    def unload_model(self) -> bool:
        """Forces Ollama to release model memory (setting keep_alive = 0)."""
        try:
            # Ollama releases a model if loaded with keep_alive=0
            requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": self.model_name,
                    "prompt": "",
                    "keep_alive": 0
                },
                timeout=5
            )
            self.model_state = "unloaded"
            logger.info(f"Model '{self.model_name}' unloaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to unload model: {e}")
            return False

    def get_lifecycle_status(self) -> dict:
        """Returns the current loading metrics of the model."""
        return {
            "model_name": self.model_name,
            "state": self.model_state,
            "warmup_duration_seconds": round(self.warmup_duration_sec, 2),
            "seconds_since_last_use": round(time.time() - self.last_used_timestamp, 1)
        }

model_lifecycle_manager = ModelLifecycleManager()
