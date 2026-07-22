import os
import uuid
import logging
import sqlite3
from datetime import datetime

import db_manager

DATA_DIR = "./data"
SQLITE_DIR = os.path.join(DATA_DIR, "sqlite")
DB_PATH = os.path.join(SQLITE_DIR, "saarthi.db")

logger = logging.getLogger("saarthi.security.audit")

class AuditTrailService:
    """
    Records immutable event history logs (queries, uploads, deletions, threat warnings)
    into a dedicated security_audit_logs SQLite database table.
    """
    
    def init_audit_db(self):
        os.makedirs(SQLITE_DIR, exist_ok=True)
        conn = db_manager.db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS security_audit_logs (
                id TEXT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                request_id TEXT,
                conversation_id TEXT,
                severity TEXT,
                event_type TEXT,
                details TEXT,
                result TEXT
            )
        """)
        conn.commit()

    def log_event(
        self, 
        event_type: str, 
        details: str, 
        result: str, 
        severity: str = "INFO", 
        request_id: str = None, 
        conversation_id: str = None
    ) -> str:
        """Writes an audit row log."""
        self.init_audit_db()
        
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        req_id = request_id or "GLOBAL"
        conv_id = conversation_id or "default"
        
        try:
            conn = db_manager.db_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO security_audit_logs (
                    id, timestamp, request_id, conversation_id, severity, event_type, details, result
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (event_id, now_str, req_id, conv_id, severity, event_type, details, result))
            conn.commit()
            logger.info(f"Audit log registered [{event_type}]: {details} (Result: {result})")
        except Exception as e:
            logger.error(f"Failed to write audit log entry: {e}")
            
        return event_id
 
    def list_audit_logs(self, limit: int = 50) -> list:
        """Fetches recent audit log rows."""
        self.init_audit_db()
        conn = db_manager.db_pool.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM security_audit_logs
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

audit_trail_service = AuditTrailService()
