# BACKEND API AUDIT

## Discovered Issues
1. **Dead Code / Unused Modules:** 
   - Multiple services in `backend/` are instantiated but never used by `main.py` (e.g., `audit_service.py`, `compliance_service.py`, `observability_service.py`).
   - *Severity:* LOW. Clutters codebase and slows down startup checks.
2. **Missing Transactional Safety:** 
   - *Severity:* HIGH. `session_manager.py` does not use explicit `BEGIN TRANSACTION` blocks for multi-table inserts (e.g., creating a conversation AND saving the first message). If the message fails, the conversation is left orphaned.
3. **Duplicate Endpoints:**
   - `main.py` contains alias endpoints (e.g., `/api/system/diagnostics` mapping to internal functions without proper prefix grouping using APIRouter).
4. **Uncaught Exceptions in Background Tasks:**
   - *Severity:* CRITICAL. The `uploadFile` background task does not catch and persist OCR errors correctly to a user-facing table, leaving the document stuck in 'Processing'.
