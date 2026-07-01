import time
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("saarthi.security.ratelimit")

class TokenBucket:
    """Token Bucket rate limiting algorithm structure."""
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = capacity
        self.fill_rate = fill_rate  # tokens per second
        self.tokens = float(capacity)
        self.last_update = time.time()

    def allow(self) -> bool:
        now = time.time()
        # Add elapsed tokens
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + (elapsed * self.fill_rate))
        self.last_update = now
        
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False


class RateLimiter:
    """
    Manages in-memory token buckets per client IP address.
    Configures specific rates for Upload, Stream, and Health routes.
    """
    
    def __init__(self):
        # buckets dict: client_ip -> TokenBucket instance
        self.upload_buckets = {}
        self.stream_buckets = {}
        self.health_buckets = {}

    def get_client_ip(self, request: Request) -> str:
        client = request.client
        return client.host if client else "127.0.0.1"

    def is_rate_limited(self, request: Request, route_type: str) -> bool:
        """
        Determines rate limits.
        Rates:
          - Upload: Capacity 5, refill 0.1/sec (1 every 10s)
          - Stream: Capacity 10, refill 0.2/sec (1 every 5s)
          - Health: Capacity 30, refill 1.0/sec (1 every 1s)
        """
        ip = self.get_client_ip(request)
        now = time.time()
        
        if route_type == "upload":
            if ip not in self.upload_buckets:
                self.upload_buckets[ip] = TokenBucket(capacity=5, fill_rate=0.1)
            return not self.upload_buckets[ip].allow()
            
        elif route_type == "stream":
            if ip not in self.stream_buckets:
                self.stream_buckets[ip] = TokenBucket(capacity=10, fill_rate=0.2)
            return not self.stream_buckets[ip].allow()
            
        else: # health / default
            if ip not in self.health_buckets:
                self.health_buckets[ip] = TokenBucket(capacity=30, fill_rate=1.0)
            return not self.health_buckets[ip].allow()

rate_limiter = RateLimiter()
