import time
import logging
import sqlite3
from typing import Callable, Any

logger = logging.getLogger("saarthi.recovery")

class CircuitBreakerOpenException(Exception):
    pass

class CircuitBreaker:
    """
    Implements a Circuit Breaker design pattern.
    Trips open if consecutive failures cross the limit, avoiding overloading services.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout_sec: float = 30.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout_sec
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.failure_count = 0
        self.last_state_change = time.time()

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.last_state_change = time.time()
            logger.error(f"Circuit breaker tripped to OPEN state! Failure count: {self.failure_count}")

    def allow_request(self) -> bool:
        if self.state == "CLOSED":
            return True
            
        now = time.time()
        if self.state == "OPEN":
            if now - self.last_state_change > self.recovery_timeout:
                self.state = "HALF-OPEN"
                logger.warning("Circuit breaker testing recovery (HALF-OPEN)...")
                return True
            return False
            
        return True  # HALF-OPEN allows test queries


class RecoveryService:
    """
    Fault recovery service containing retry loops, exponential backoffs,
    and circuit breakers for database pools and local model connections.
    """
    def __init__(self):
        self.db_breaker = CircuitBreaker()
        self.ollama_breaker = CircuitBreaker()
        self.recovery_events = []

    def execute_db_query(self, query_fn: Callable[[], Any], max_retries: int = 5) -> Any:
        """
        Executes a database query function wrapped in a retry backoff loop.
        """
        if not self.db_breaker.allow_request():
            raise CircuitBreakerOpenException("Database circuit breaker is currently OPEN.")

        backoff = 0.05
        for attempt in range(1, max_retries + 1):
            try:
                res = query_fn()
                self.db_breaker.record_success()
                return res
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < max_retries:
                    logger.warning(f"Database locked. Retry attempt {attempt}/{max_retries} after {backoff}s...")
                    time.sleep(backoff)
                    backoff *= 2.0  # exponential backoff
                else:
                    self.db_breaker.record_failure()
                    self.log_recovery_event("db_lock_failure", str(e))
                    raise e
            except Exception as e:
                self.db_breaker.record_failure()
                self.log_recovery_event("db_generic_failure", str(e))
                raise e

    def execute_ollama_call(self, call_fn: Callable[[], Any], max_retries: int = 3) -> Any:
        """
        Executes a local LLM call wrapped in a retry backoff loop.
        """
        if not self.ollama_breaker.allow_request():
            raise CircuitBreakerOpenException("Ollama LLM circuit breaker is currently OPEN.")

        backoff = 1.0
        for attempt in range(1, max_retries + 1):
            try:
                res = call_fn()
                self.ollama_breaker.record_success()
                return res
            except Exception as e:
                logger.warning(f"Ollama call failed: {e}. Attempt {attempt}/{max_retries}...")
                if attempt < max_retries:
                    time.sleep(backoff)
                    backoff *= 1.5
                else:
                    self.ollama_breaker.record_failure()
                    self.log_recovery_event("ollama_timeout_failure", str(e))
                    raise e

    def log_recovery_event(self, event_type: str, error_msg: str):
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "error": error_msg
        }
        self.recovery_events.append(event)
        # Cap events log
        self.recovery_events = self.recovery_events[-20:]

    def get_recovery_status(self) -> dict:
        return {
            "db_circuit_breaker_state": self.db_breaker.state,
            "ollama_circuit_breaker_state": self.ollama_breaker.state,
            "recent_recovery_events": self.recovery_events
        }

recovery_service = RecoveryService()
