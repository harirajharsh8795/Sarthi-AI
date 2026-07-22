# CITATION ENGINE AUDIT

## Pipeline Flaws
1. **Excerpt Truncation:**
   - *Severity:* LOW. The `text_preview` added in Sprint 6 can theoretically be thousands of characters long. The backend does not truncate it, meaning massive payloads are sent over SSE for simple citations.
2. **Regex Spoofing:**
   - *Severity:* MEDIUM. `output_validator.py` uses naive regex `\[(\d+)\]` to find citations. If the LLM generates a code block containing an array like `arr[1]`, the validator will mistake it for a citation and strip it.
