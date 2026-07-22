# PERFORMANCE AUDIT

## Pipeline Flaws
1. **React Re-Renders:**
   - *Severity:* HIGH. Typing in `InputArea.jsx` triggers a re-render of the entire `ChatWorkspace.jsx` because `input` is hoisted to the parent without memoization of `ChatMessages.jsx`. This makes typing lag on long conversations.
2. **Vector DB Bloat:**
   - *Severity:* MEDIUM. ChromaDB collections are never compacted or garbage-collected after documents are deleted, leading to infinite disk growth.
