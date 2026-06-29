import time
import statistics
import threading
import logging
from db_manager import get_db_cursor

logger = logging.getLogger("saarthi.metrics")

class MetricsManager:
    """
    Central Metrics collector tracking latencies and computing statistical windows.
    Thread-safe implementation with local collections.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(MetricsManager, cls).__new__(cls, *args, **kwargs)
                    cls._instance._init_metrics()
        return cls._instance

    def _init_metrics(self):
        # Keep list of last 100 timings for each category
        self.metrics = {
            "ocr_time": [],
            "embedding_time": [],
            "retrieval_time": [],
            "inference_time": [],
            "upload_time": []
        }
        self.metric_lock = threading.Lock()

    def record(self, category: str, duration_sec: float):
        """Records a metric duration in seconds."""
        if category not in self.metrics:
            return
            
        duration_ms = duration_sec * 1000.0
        with self.metric_lock:
            self.metrics[category].append(duration_ms)
            if len(self.metrics[category]) > 100:
                self.metrics[category].pop(0)
                
        logger.info(f"Recorded performance metric [{category}]: {duration_ms:.2f}ms")

    def get_summary(self, category: str) -> dict:
        """Computes min, max, average, and P95 latency stats."""
        if category not in self.metrics:
            return {}
            
        with self.metric_lock:
            data = list(self.metrics[category])
            
        if not data:
            return {"min": 0, "max": 0, "avg": 0, "p95": 0}
            
        data.sort()
        n = len(data)
        
        avg_val = sum(data) / n
        min_val = data[0]
        max_val = data[-1]
        
        # P95 percentile calculation
        p95_idx = max(0, min(n - 1, int(n * 0.95)))
        p95_val = data[p95_idx]
        
        return {
            "min": round(min_val, 2),
            "max": round(max_val, 2),
            "avg": round(avg_val, 2),
            "p95": round(p95_val, 2)
        }

    def get_all_summaries(self) -> dict:
        """Returns all aggregated metrics summaries."""
        return {k: self.get_summary(k) for k in self.metrics.keys()}

metrics_manager = MetricsManager()
