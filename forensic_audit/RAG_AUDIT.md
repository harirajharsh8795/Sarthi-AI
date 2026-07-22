# RAG PIPELINE AUDIT

## Pipeline Flaws
1. **Cross-Contamination Risk:**
   - *Severity:* HIGH. User documents are added to a shared ChromaDB collection. While `collection` tags exist, strict row-level isolation via tenant IDs is missing, posing a risk if the frontend spoofed a request.
2. **Chunking Overlap:**
   - *Severity:* LOW. The chunking logic in `kb_pipeline.py` uses rigid token boundaries, which frequently cuts sentences in half, causing the `validation_service.py` to incorrectly mark valid claims as unsupported.
3. **Vector Distance Threshold:**
   - *Severity:* MEDIUM. The cosine similarity cutoff in `retrieval_router.py` is too permissive, resulting in irrelevant chunks being appended to the prompt, wasting context window and increasing hallucination risk.
