# SYSTEM ARCHITECTURE AUDIT

## Overview
Saarthi AI is built as a split monolithic architecture with a React frontend (Vite) and a FastAPI backend (Python).
- **Frontend:** React + Vite, styling via Tailwind/Vanilla CSS.
- **Backend:** FastAPI, Uvicorn, SQLite for persistence, ChromaDB for vector storage.
- **AI Engine:** LangChain/Custom LLM inference pipelines for RAG.
- **Background Tasks:** ThreadPoolExecutor / Asyncio tasks.

## Architectural Flaws
1. **State Duplication:** The frontend React state is heavily duplicated across `ChatWorkspace.jsx`, `InputArea.jsx`, and `App.jsx`.
2. **Coupled Lifecycles:** Streaming, history saving, and conversation creation are tightly bound to the UI lifecycle instead of an isolated background service worker.
3. **Missing Message Queue:** No robust task queue (like Celery/Redis) exists for heavy operations (OCR, Embedding, LLM inference). Instead, it relies on in-memory async tasks which vanish on server restart.
4. **No True Database ORM:** Raw SQLite queries and basic helper functions in `session_manager.py` lead to connection locking and missing transactional safety.
5. **No WebSocket:** The system relies on SSE (Server-Sent Events) for downstream streaming, but standard HTTP for upstream requests, leading to desynced states during network drops.
