# SECURITY AUDIT

## Pipeline Flaws
1. **Path Traversal Risk:**
   - *Severity:* CRITICAL. The `uploadFile` endpoint does not strictly sanitize the `filename` before saving to disk. A malicious payload with `filename="../../../etc/passwd"` could overwrite system files.
2. **Missing Rate Limiting:**
   - *Severity:* HIGH. The `/api/stream` endpoint has no strict IP or User-level rate limiting, making the application highly susceptible to DoS attacks via LLM token exhaustion.
