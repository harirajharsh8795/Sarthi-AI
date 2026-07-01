import os
import sqlite3
import time
import logging
from contextlib import contextmanager
from config import settings

logger = logging.getLogger("saarthi.db")

class DBConnectionPool:
    """Thread-safe lazy-loaded connection pool/cache for SQLite."""
    _instance = None
    _connections = {}  # Thread-ID to connection mapping
    _lock = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            import threading
            cls._lock = threading.Lock()
            cls._instance = super(DBConnectionPool, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_connection(self) -> sqlite3.Connection:
        import threading
        thread_id = threading.get_ident()
        
        # Fast path
        if thread_id in self._connections:
            # Check if active connection is closed or corrupted
            try:
                self._connections[thread_id].execute("SELECT 1")
                return self._connections[thread_id]
            except (sqlite3.ProgrammingError, sqlite3.OperationalError):
                del self._connections[thread_id]
                
        with self._lock:
            # Ensure folder is present
            os.makedirs(settings.SQLITE_DIR, exist_ok=True)
            
            conn = sqlite3.connect(
                settings.DB_PATH,
                timeout=settings.DB_TIMEOUT,
                check_same_thread=False
            )
            conn.row_factory = sqlite3.Row
            
            # Enable WAL mode & foreign keys
            if settings.ENABLE_WAL_MODE:
                conn.execute("PRAGMA journal_mode=WAL;")
            if settings.ENABLE_DB_FOREIGN_KEYS:
                conn.execute("PRAGMA foreign_keys=ON;")
                
            self._connections[thread_id] = conn
            return conn

    def close_all(self):
        """Shutdown helper to close all connections in pool."""
        with self._lock:
            for tid, conn in list(self._connections.items()):
                try:
                    conn.close()
                except Exception:
                    pass
            self._connections.clear()
            logger.info("All SQLite pool connections closed gracefully.")

db_pool = DBConnectionPool()

@contextmanager
def get_db_cursor(read_only: bool = False):
    """
    Context manager providing a transactional cursor.
    Handles transaction commit/rollback, connection acquisition, and failures automatically.
    """
    conn = db_pool.get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        if not read_only:
            conn.commit()
    except Exception as e:
        if not read_only:
            try:
                conn.rollback()
                logger.warning("DB transaction rolled back due to error.")
            except Exception:
                pass
        raise e
    finally:
        cursor.close()

def execute_with_retry(query: str, params: tuple = (), retries: int = 3, delay: float = 0.5):
    """
    Wrapper offering retry semantics on operational locking warnings.
    """
    for attempt in range(retries):
        try:
            with get_db_cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except sqlite3.OperationalError as oe:
            if "locked" in str(oe).lower() and attempt < retries - 1:
                sleep_time = delay * (2 ** attempt)
                logger.warning(f"Database locked. Attempt {attempt + 1} retrying in {sleep_time}s...")
                time.sleep(sleep_time)
            else:
                raise oe
