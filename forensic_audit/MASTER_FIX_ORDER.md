# MASTER FIX ORDER & ROADMAP

To reach production readiness without breaking existing modules, implement fixes in this EXACT order:

## Phase 1: Core Stability (Backend)
1. **Enable WAL Mode in SQLite:** Fixes `database is locked` concurrency errors.
2. **Add AbortSignal Support to SSE:** Prevents runaway LLM token generation on disconnect.
3. **Fix Path Traversal in Upload:** Sanitize filenames securely.

## Phase 2: State Machine (Frontend)
4. **Remove Duplicate Components:** Delete `frontend/src/components/MessageBubble.jsx`.
5. **Memoize ChatMessages:** Use `React.memo` to prevent typing lag.
6. **Fix SSE Conversation Bleed:** Ensure incoming packets are scoped to `conversationId`.

## Phase 3: RAG & AI Robustness
7. **Refine Chunking Strategy:** Stop splitting in the middle of sentences.
8. **Fix Regex Spoofing in Citations:** Use AST or strict boundaries for `[1]` detection instead of loose regex.
9. **Implement Job Queue Persistence:** Use SQLite or Redis for upload jobs so they survive server restarts.

## Phase 4: Cleanup
10. **Remove Dead Services:** Delete `audit_service.py`, `compliance_service.py`, etc.
11. **Enforce Rate Limiting:** Protect the LLM pipeline from exhaustion.
