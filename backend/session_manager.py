import os
import sqlite3
from datetime import datetime

DATA_DIR = "./data"
SQLITE_DIR = os.path.join(DATA_DIR, "sqlite")
DB_PATH = os.path.join(SQLITE_DIR, "saarthi.db")

import db_manager

def get_db_connection():
    """Returns a connection to the SQLite database with Row factory enabled."""
    return db_manager.db_pool.get_connection()

def init_session_db():
    """Initializes the SQLite tables for user sessions, documents, conversations, and messages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create user_sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_sessions (
            session_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            display_name TEXT
        )
    """)
    
    # Create user_documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_documents (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            conversation_id TEXT,
            original_filename TEXT,
            file_type TEXT,
            domain_hint TEXT,
            ocr_used BOOLEAN,
            page_count INTEGER,
            chunk_count INTEGER,
            status TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            indexed_at TIMESTAMP,
            ocr_confidence REAL,
            ocr_low_quality_warning BOOLEAN,
            FOREIGN KEY (session_id) REFERENCES user_sessions (session_id),
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)
    
    # Create conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            session_id TEXT,
            title TEXT,
            message_count INTEGER DEFAULT 0,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES user_sessions (session_id)
        )
    """)
    
    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT,
            role TEXT CHECK(role IN ('user','assistant')),
            content TEXT,
            citations TEXT, -- JSON array stored as string
            created_at TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)
    
    # Add columns via ALTER TABLE if the database already exists
    try:
        cursor.execute("ALTER TABLE user_documents ADD COLUMN ocr_confidence REAL;")
    except sqlite3.OperationalError:
        pass  # Column already exists
        
    try:
        cursor.execute("ALTER TABLE user_documents ADD COLUMN ocr_low_quality_warning BOOLEAN;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute("ALTER TABLE user_documents ADD COLUMN conversation_id TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute("ALTER TABLE user_documents ADD COLUMN file_hash TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists

    try:
        cursor.execute("ALTER TABLE conversations ADD COLUMN device_id TEXT;")
    except sqlite3.OperationalError:
        pass  # Column already exists
        
    conn.commit()
    conn.close()
    logger.debug("SQLite session tables initialized successfully.")

def get_or_create_session(session_id, display_name=None):
    """
    Retrieves or creates a session. Updates the last_active_at timestamp.
    Returns the session row as a dictionary.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    cursor.execute("SELECT * FROM user_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("""
            UPDATE user_sessions 
            SET last_active_at = ? 
            WHERE session_id = ?
        """, (now_str, session_id))
        conn.commit()
    else:
        cursor.execute("""
            INSERT INTO user_sessions (session_id, created_at, last_active_at, display_name)
            VALUES (?, ?, ?, ?)
        """, (session_id, now_str, now_str, display_name))
        conn.commit()
        
    cursor.execute("SELECT * FROM user_sessions WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    res = dict(row)
    conn.close()
    return res

def create_document_record(document_id, session_id, original_filename, file_type, 
                           domain_hint=None, ocr_used=False, page_count=None, 
                           chunk_count=None, status="pending", ocr_confidence=None, 
                           ocr_low_quality_warning=None, conversation_id=None, file_hash=None):
    """
    Inserts a new user document record.
    If the document already exists, raises an error or handles it.
    """
    # Ensure the session exists
    get_or_create_session(session_id)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    # Check for existing document
    cursor.execute("SELECT id FROM user_documents WHERE id = ?", (document_id,))
    existing = cursor.fetchone()
    
    ocr_low_quality_val = int(ocr_low_quality_warning) if ocr_low_quality_warning is not None else None
    
    if existing:
        # Upsert-like behavior: update existing details
        cursor.execute("""
            UPDATE user_documents
            SET session_id = ?, conversation_id = ?, original_filename = ?, file_type = ?, domain_hint = ?,
                ocr_used = ?, page_count = ?, chunk_count = ?, status = ?, uploaded_at = ?,
                ocr_confidence = ?, ocr_low_quality_warning = ?, file_hash = ?
            WHERE id = ?
        """, (session_id, conversation_id, original_filename, file_type, domain_hint, int(ocr_used), 
              page_count, chunk_count, status, now_str, ocr_confidence, ocr_low_quality_val, file_hash, document_id))
    else:
        cursor.execute("""
            INSERT INTO user_documents 
            (id, session_id, conversation_id, original_filename, file_type, domain_hint, ocr_used, page_count, chunk_count, status, uploaded_at, ocr_confidence, ocr_low_quality_warning, file_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (document_id, session_id, conversation_id, original_filename, file_type, domain_hint, int(ocr_used), page_count, chunk_count, status, now_str, ocr_confidence, ocr_low_quality_val, file_hash))
        
    conn.commit()
    conn.close()

def update_document_status(document_id, session_id, status, page_count=None, chunk_count=None, indexed_at=None, ocr_confidence=None, ocr_low_quality_warning=None):
    """Updates the status and indexing metadata of an uploaded document."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = ["status = ?"]
    params = [status]
    
    if page_count is not None:
        update_fields.append("page_count = ?")
        params.append(page_count)
    if chunk_count is not None:
        update_fields.append("chunk_count = ?")
        params.append(chunk_count)
    if indexed_at is not None:
        update_fields.append("indexed_at = ?")
        params.append(indexed_at)
    else:
        if status == "indexed":
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            update_fields.append("indexed_at = ?")
            params.append(now_str)
            
    if ocr_confidence is not None:
        update_fields.append("ocr_confidence = ?")
        params.append(ocr_confidence)
    if ocr_low_quality_warning is not None:
        update_fields.append("ocr_low_quality_warning = ?")
        params.append(int(ocr_low_quality_warning))
            
    params.extend([document_id, session_id])
    
    query = f"""
        UPDATE user_documents 
        SET {', '.join(update_fields)} 
        WHERE id = ? AND session_id = ?
    """
    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

def delete_document_record(document_id, session_id):
    """
    Performs a soft-delete of the document record in SQLite.
    Sets status = 'deleted'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM user_documents 
        WHERE id = ? AND session_id = ?
    """, (document_id, session_id))
    conn.commit()
    conn.close()

def get_document_record(document_id, session_id):
    """Retrieves a document record if it exists and belongs to the session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM user_documents 
        WHERE id = ? AND session_id = ?
    """, (document_id, session_id))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_session_documents(session_id, include_deleted=False, conversation_id=None):
    """
    Retrieves all documents associated with a session (and optionally a specific conversation).
    By default, filters out deleted documents.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if conversation_id:
        if include_deleted:
            cursor.execute("SELECT * FROM user_documents WHERE session_id = ? AND conversation_id = ?", (session_id, conversation_id))
        else:
            cursor.execute("SELECT * FROM user_documents WHERE session_id = ? AND conversation_id = ? AND status != 'deleted'", (session_id, conversation_id))
    else:
        if include_deleted:
            cursor.execute("SELECT * FROM user_documents WHERE session_id = ?", (session_id,))
        else:
            cursor.execute("SELECT * FROM user_documents WHERE session_id = ? AND status != 'deleted'", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def list_session_documents(session_id: str, conversation_id: str = None) -> list:
    """Retrieves all non-deleted documents for a session/conversation, ordered by uploaded_at descending."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if conversation_id:
        cursor.execute("""
            SELECT id as document_id, original_filename, file_type, page_count, chunk_count, ocr_used, status, uploaded_at
            FROM user_documents
            WHERE session_id = ? AND conversation_id = ? AND status != 'deleted'
            ORDER BY uploaded_at DESC
        """, (session_id, conversation_id))
    else:
        cursor.execute("""
            SELECT id as document_id, original_filename, file_type, page_count, chunk_count, ocr_used, status, uploaded_at
            FROM user_documents
            WHERE session_id = ? AND status != 'deleted'
            ORDER BY uploaded_at DESC
        """, (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ==========================================
# Conversation History Management Helpers
# ==========================================

import json
from logger_config import logger

def list_conversations(session_id):
    """Retrieves all conversations for a session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, message_count, created_at, updated_at
        FROM conversations
        WHERE session_id = ?
        ORDER BY updated_at DESC
    """, (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def list_all_conversations(device_id):
    """Retrieves all conversations for a specific device_id."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, message_count, created_at, updated_at
        FROM conversations
        WHERE device_id = ?
        ORDER BY updated_at DESC
    """, (device_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_conversation_messages(conversation_id: str) -> list:
    """Retrieves all messages for a conversation, ordered by created_at ascending."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, conversation_id, role, content, citations, created_at
        FROM messages
        WHERE conversation_id = ?
        ORDER BY created_at ASC
    """, (conversation_id,))
    rows = cursor.fetchall()
    conn.close()
    
    res = []
    for r in rows:
        d = dict(r)
        if d.get("citations"):
            try:
                d["citations"] = json.loads(d["citations"])
            except Exception:
                d["citations"] = []
        else:
            d["citations"] = []
        res.append(d)
    return res

def create_conversation(conversation_id: str, session_id: str, title: str = "New Conversation", device_id: str = None) -> str:
    """Creates a new conversation record in SQLite."""
    get_or_create_session(session_id)
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    cursor.execute("""
        INSERT INTO conversations (id, session_id, title, message_count, created_at, updated_at, device_id)
        VALUES (?, ?, ?, 0, ?, ?, ?)
    """, (conversation_id, session_id, title[:100], now_str, now_str, device_id))
    conn.commit()
    conn.close()
    return conversation_id

def save_message(message_id: str, conversation_id: str, role: str, content: str, citations: list = None) -> None:
    """
    Saves a message to SQLite. Automatically increments message_count in conversations.
    If it is the first user message, automatically updates the conversation title to match.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    citations_str = json.dumps(citations) if citations is not None else "[]"
    
    # 1. Save the message record
    cursor.execute("""
        INSERT INTO messages (id, conversation_id, role, content, citations, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (message_id, conversation_id, role, content, citations_str, now_str))
    
    # 2. Check message count to decide on title update
    cursor.execute("SELECT message_count FROM conversations WHERE id = ?", (conversation_id,))
    row = cursor.fetchone()
    
    if row:
        current_count = row["message_count"]
        # If this is the first user message, update the title to the message content (max 100 chars)
        if role == "user" and current_count == 0:
            cursor.execute("""
                UPDATE conversations
                SET title = ?, message_count = message_count + 1, updated_at = ?
                WHERE id = ?
            """, (content[:100], now_str, conversation_id))
        else:
            cursor.execute("""
                UPDATE conversations
                SET message_count = message_count + 1, updated_at = ?
                WHERE id = ?
            """, (now_str, conversation_id))
            
    conn.commit()
    conn.close()


def delete_conversation(conversation_id: str, session_id: str) -> list:
    """
    Deletes all messages and documents associated with the conversation,
    and then deletes the conversation metadata record.
    Returns a list of document IDs that need their vector store chunks removed.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Fetch document IDs to return to caller for vector cleanup
    cursor.execute(
        "SELECT id FROM user_documents WHERE session_id = ? AND conversation_id = ?",
        (session_id, conversation_id)
    )
    doc_ids = [row["id"] for row in cursor.fetchall()]
    
    # 2. Delete messages in the conversation
    cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
    
    # 3. Hard-delete documents in database
    cursor.execute(
        "DELETE FROM user_documents WHERE session_id = ? AND conversation_id = ?",
        (session_id, conversation_id)
    )
    
    # 4. Delete conversation row
    cursor.execute("DELETE FROM conversations WHERE id = ? AND session_id = ?", (conversation_id, session_id))
    
    conn.commit()
    conn.close()
    return doc_ids


def delete_messages_after(conversation_id: str, message_id: str) -> int:
    """
    Deletes the target message and any subsequent messages in the conversation.
    Updates the conversation message count.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Get the creation time of the target message
    cursor.execute("SELECT created_at FROM messages WHERE id = ?", (message_id,))
    target = cursor.fetchone()
    if not target:
        conn.close()
        return 0
        
    target_time = target["created_at"]
    
    # 2. Delete all messages created at or after this message time in the conversation
    cursor.execute(
        "DELETE FROM messages WHERE conversation_id = ? AND created_at >= ?",
        (conversation_id, target_time)
    )
    deleted_count = cursor.rowcount
    
    # 3. Re-count remaining messages and update the conversation
    cursor.execute("SELECT COUNT(*) as cnt FROM messages WHERE conversation_id = ?", (conversation_id,))
    cnt_row = cursor.fetchone()
    remaining = cnt_row["cnt"] if cnt_row else 0
    
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    cursor.execute(
        "UPDATE conversations SET message_count = ?, updated_at = ? WHERE id = ?",
        (remaining, now_str, conversation_id)
    )
    
    conn.commit()
    conn.close()
    return deleted_count


def search_messages(session_id: str, query: str, limit: int = 20) -> list:
    """
    Performs full-text SQL search across all messages in a user session.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    search_pattern = f"%{query}%"
    cursor.execute(
        """
        SELECT m.id as message_id, m.conversation_id, c.title, m.content, m.role, m.created_at
        FROM messages m
        JOIN conversations c ON m.conversation_id = c.id
        WHERE c.session_id = ? AND m.content LIKE ?
        ORDER BY m.created_at DESC
        LIMIT ?
        """,
        (session_id, search_pattern, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        d = dict(r)
        # Create snippet
        content = d.get("content", "")
        d["snippet"] = content[:200]
        results.append(d)
    return results


