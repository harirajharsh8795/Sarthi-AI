import os
import sys
import pytest
import sqlite3
import threading
import time
from fastapi.testclient import TestClient

# Add parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from db_manager import db_pool, get_db_cursor, execute_with_retry
from services import chroma_manager, embedding_service
from job_queue import job_queue
from main import app, SaarthiError

client = TestClient(app)

def test_sqlite_singleton_and_wal():
    """Verifies that connections in pool resolve WAL mode and foreign keys."""
    conn = db_pool.get_connection()
    assert isinstance(conn, sqlite3.Connection)
    
    # Verify WAL journal mode
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode;")
    mode = cursor.fetchone()[0]
    assert mode.lower() == "wal"
    
    # Verify Foreign Keys
    cursor.execute("PRAGMA foreign_keys;")
    fkey = cursor.fetchone()[0]
    assert fkey == 1

def test_database_concurrency():
    """Spawns 5 threads performing concurrent writes to verify lock safety."""
    # Create test table
    with get_db_cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS test_concurrency (id TEXT PRIMARY KEY, val TEXT)")
        cursor.execute("DELETE FROM test_concurrency")
        
    errors = []
    
    def worker(worker_id):
        try:
            for i in range(10):
                row_id = f"worker_{worker_id}_row_{i}"
                with get_db_cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO test_concurrency (id, val) VALUES (?, ?)", 
                        (row_id, f"val_{i}")
                    )
                time.sleep(0.01)
        except Exception as e:
            errors.append(e)
            
    threads = []
    for t_id in range(5):
        t = threading.Thread(target=worker, args=(t_id,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    # Check for any concurrency exceptions
    assert len(errors) == 0, f"Concurrent database writes raised errors: {errors}"
    
    # Cleanup test table
    with get_db_cursor() as cursor:
        cursor.execute("DROP TABLE test_concurrency")

def test_chroma_client_singleton():
    """Validates that ChromaDB persistent client resolves correctly."""
    c1 = chroma_manager.get_client()
    c2 = chroma_manager.get_client()
    assert c1 is c2
    
    coll1 = chroma_manager.get_collection("knowledge_base")
    coll2 = chroma_manager.get_collection("knowledge_base")
    assert coll1 is coll2

def test_job_queue_status_progression():
    """Creates a job and tests manual progression states."""
    job_id = job_queue.create_job("doc_test_123", "conv_test_123")
    assert job_id.startswith("job_")
    
    # Verify initial state
    job = job_queue.get_job(job_id)
    assert job["status"] == "queued"
    assert job["progress"] == 0
    
    # Update state
    job_queue.update_job(job_id, "running", 50, "Embedding")
    job = job_queue.get_job(job_id)
    assert job["status"] == "running"
    assert job["progress"] == 50
    assert job["step"] == "Embedding"
    
    # Complete job
    job_queue.update_job(job_id, "completed", 100, "Ready")
    job = job_queue.get_job(job_id)
    assert job["status"] == "completed"
    assert job["progress"] == 100

def test_health_endpoint_response():
    """Verifies health check endpoint schema structure."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    
    assert "ollama_status" in data
    assert "sqlite_status" in data
    assert "chroma_status" in data
    assert "kb_chunks" in data
    assert "cpu_usage_pct" in data
    assert "memory_usage_pct" in data
