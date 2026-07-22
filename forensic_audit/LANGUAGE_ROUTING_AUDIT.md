# LANGUAGE ROUTING AUDIT

## Pipeline Flaws
1. **Hinglish Detection Failure:**
   - *Severity:* MEDIUM. The intent engine relies on rigid regex or basic language detection libraries. Hinglish (Hindi written in English script) is frequently misclassified as English, causing the LLM to reply in English instead of Hinglish.
2. **Prompt Dilution:**
   - Instructing the model to "reply in Hindi" inside the system prompt often conflicts with the retrieved English RAG context, causing the model to output mixed languages.
