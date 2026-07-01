import uuid
import logging
import threading
from typing import Optional
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from db_manager import get_db_cursor
from config import settings

logger = logging.getLogger("saarthi.jobs")

class JobQueueManager:
    """
    Manages background document ingestion tasks (OCR, embedding, indexing)
    using SQLite database for state persistence and a ThreadPoolExecutor.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(JobQueueManager, cls).__new__(cls, *args, **kwargs)
                    cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        # Allow up to 2 concurrent ingestion pipelines
        self.executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="SaarthiJob")
        self._init_db()

    def _init_db(self):
        """Initializes the background_jobs status table."""
        with get_db_cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS background_jobs (
                    job_id TEXT PRIMARY KEY,
                    document_id TEXT,
                    conversation_id TEXT,
                    status TEXT,
                    progress INTEGER,
                    step TEXT,
                    error_message TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP
                )
            """)

    def create_job(self, document_id: str, conversation_id: str) -> str:
        """Creates a new job and inserts it into database."""
        job_id = f"job_{uuid.uuid4().hex[:8]}"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with get_db_cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO background_jobs (job_id, document_id, conversation_id, status, progress, step, start_time)
                VALUES (?, ?, ?, 'queued', 0, 'Queued', ?)
                """,
                (job_id, document_id, conversation_id, now_str)
            )
        logger.info(f"Created background job {job_id} for document {document_id}")
        return job_id

    def update_job(self, job_id: str, status: str, progress: int, step: str, error_message: str = None):
        """Updates job status and progress in SQLite."""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if status in ("completed", "failed", "cancelled") else None
        
        with get_db_cursor() as cursor:
            if now_str:
                cursor.execute(
                    """
                    UPDATE background_jobs 
                    SET status = ?, progress = ?, step = ?, error_message = ?, end_time = ?
                    WHERE job_id = ?
                    """,
                    (status, progress, step, error_message, now_str, job_id)
                )
            else:
                cursor.execute(
                    """
                    UPDATE background_jobs 
                    SET status = ?, progress = ?, step = ?, error_message = ?
                    WHERE job_id = ?
                    """,
                    (status, progress, step, error_message, job_id)
                )
        logger.info(f"Updated job {job_id} -> status={status}, progress={progress}%, step='{step}'")

    def get_job(self, job_id: str) -> Optional[dict]:
        """Retrieves current job status details."""
        with get_db_cursor(read_only=True) as cursor:
            cursor.execute("SELECT * FROM background_jobs WHERE job_id = ?", (job_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def submit_task(self, fn, *args, **kwargs):
        """Submits task function to thread pool."""
        return self.executor.submit(fn, *args, **kwargs)

    def shutdown(self):
        """Shutdown helper to cancel pending tasks and release workers."""
        logger.info("Shutting down JobQueue thread pool executor...")
        self.executor.shutdown(wait=False, cancel_futures=True)
        logger.info("JobQueue thread pool executor released.")

job_queue = JobQueueManager()
