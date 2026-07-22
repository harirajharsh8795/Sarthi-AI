# DATA FLOW AUDIT

## Complete Data Flow Map
**User Input** -> `InputArea.jsx` -> `ChatWorkspace.jsx` (React State update) -> `fetch` to `/api/stream` 
-> `main.py` -> `llm_inference.py` -> `query_planner.py` -> `retrieval_router.py` 
-> `ChromaDB` (Vector Search) -> `prompt_builder.py` -> LLM API -> `validation_service.py` 
-> `output_validator.py` -> SSE Stream back to `ChatWorkspace.jsx` -> `MarkdownRenderer.jsx`

## Critical Data Flow Flaws
1. **Loss of Excerpt in Pipeline:** The RAG pipeline retrieves the document chunk, but `llm_inference.py` drops the `text` attribute before formatting the `citation` payload for the frontend.
2. **Validation Mutilation:** Data flows through `validation_service.py` which structurally mutates the generated text (destroying markdown) before persisting it to the DB, causing history to differ from the live SSE stream.
3. **Dual Source of Truth:** `App.jsx` and `session_manager.py` both attempt to maintain conversation lists, leading to desyncs if the frontend fails to reload after a backend change.
