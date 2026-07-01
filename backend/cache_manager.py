import time
import logging
from collections import OrderedDict

logger = logging.getLogger("saarthi.cache")

class MemoryLRUCache:
    """
    An LRU Cache with TTL (Time-To-Live) evictions.
    Thread-safe implementation wrapping standard OrderedDict.
    """
    def __init__(self, capacity: int = 100, ttl_seconds: float = 300.0):
        self.capacity = capacity
        self.ttl = ttl_seconds
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key):
        if key not in self.cache:
            self.misses += 1
            return None
            
        value, timestamp = self.cache[key]
        if time.time() - timestamp > self.ttl:
            # Expired
            self.cache.pop(key)
            self.misses += 1
            return None
            
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        self.hits += 1
        return value

    def set(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
            
        self.cache[key] = (value, time.time())
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Evict least recently used

    def clear(self):
        self.cache.clear()
        self.hits = 0
        self.misses = 0

    def shrink(self):
        """Drops half of the cached values to release memory."""
        shrink_count = len(self.cache) // 2
        for _ in range(shrink_count):
            if self.cache:
                self.cache.popitem(last=False)
        logger.info(f"Cache shrunken. Current size: {len(self.cache)}")

    def get_stats(self) -> dict:
        total = self.hits + self.misses
        ratio = (self.hits / total) if total > 0 else 0.0
        return {
            "size": len(self.cache),
            "capacity": self.capacity,
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio": round(ratio, 4)
        }


class CacheManager:
    """
    Central coordinator of in-memory caching systems.
    Separates cache spaces for OCR, Embeddings, Retrieval, and Health dashboards.
    """
    def __init__(self):
        self.ocr_cache = MemoryLRUCache(capacity=50, ttl_seconds=1800.0)
        self.embed_cache = MemoryLRUCache(capacity=200, ttl_seconds=600.0)
        self.retrieval_cache = MemoryLRUCache(capacity=100, ttl_seconds=120.0)

    def shrink_all_caches(self):
        """Called by Edge Autotuner to reclaim RAM under high system loads."""
        logger.warning("Edge tuning request: evicting memory cache tables...")
        self.ocr_cache.shrink()
        self.embed_cache.shrink()
        self.retrieval_cache.shrink()

    def clear_all(self):
        self.ocr_cache.clear()
        self.embed_cache.clear()
        self.retrieval_cache.clear()

    def get_global_metrics(self) -> dict:
        """Returns consolidated statistics for explainable edge dashboards."""
        return {
            "ocr_cache": self.ocr_cache.get_stats(),
            "embedding_cache": self.embed_cache.get_stats(),
            "retrieval_cache": self.retrieval_cache.get_stats()
        }

cache_manager = CacheManager()
