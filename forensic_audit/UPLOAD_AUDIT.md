# UPLOAD PIPELINE AUDIT

## Pipeline Flaws
1. **Zombie Jobs:**
   - *Severity:* MEDIUM. If the server restarts during an upload, the `job_queue` (which is in-memory) is wiped. The UI will poll infinitely for a `job_id` that no longer exists.
2. **File Name Collisions:**
   - *Severity:* LOW. If a user uploads "invoice.pdf" twice, the backend overwrites the internal file path or confuses the ChromaDB metadata due to lack of UUID generation for physical storage.
