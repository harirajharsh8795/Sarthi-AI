import time
import logging
from collections import deque

logger = logging.getLogger("saarthi.observability")

class ObservabilityService:
    """
    Tracks request rate, error rate, queue sizes, and current generation
    streams to provide complete runtime system logs.
    """
    
    def __init__(self):
        # 1-minute tracking window (timestamps of requests and errors)
        self.request_timestamps = deque()
        self.error_timestamps = deque()
        self.latency_buffer = deque(maxlen=20)  # rolling average of last 20 queries

    def record_request(self):
        self.request_timestamps.append(time.time())

    def record_error(self):
        self.error_timestamps.append(time.time())

    def record_latency(self, duration_ms: float):
        self.latency_buffer.append(duration_ms)

    def clean_old_timestamps(self, now: float):
        # Slide 1 minute window
        boundary = now - 60.0
        while self.request_timestamps and self.request_timestamps[0] < boundary:
            self.request_timestamps.popleft()
        while self.error_timestamps and self.error_timestamps[0] < boundary:
            self.error_timestamps.popleft()

    def get_observability_metrics(self) -> dict:
        """Compiles requests per minute, error rate, and worker queue metrics."""
        now = time.time()
        self.clean_old_timestamps(now)
        
        # Calculate rates
        rpm = len(self.request_timestamps)
        epm = len(self.error_timestamps)
        
        avg_latency = sum(self.latency_buffer) / len(self.latency_buffer) if self.latency_buffer else 0.0
        
        # Active counts from singleton pools
        from job_queue import job_queue
        from main import active_streams
        
        pending_jobs = sum(1 for j in job_queue.jobs.values() if j["status"] in ["queued", "running"])
        
        return {
            "timestamp": time.strftime("%H:%M:%S"),
            "requests_per_minute": rpm,
            "errors_per_minute": epm,
            "average_latency_ms": round(avg_latency, 2),
            "active_streams_count": len(active_streams),
            "queued_jobs_count": pending_jobs,
            "jobs_queue_status": "idle" if pending_jobs == 0 else "busy"
        }

observability_service = ObservabilityService()
