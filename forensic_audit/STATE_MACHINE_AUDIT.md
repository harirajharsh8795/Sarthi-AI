# STATE MACHINE AUDIT

## Pipeline Flaws
1. **Conflicting Boolean Flags:**
   - `ChatWorkspace.jsx` uses `isStreaming`, `uploadingFile`, `transcribing`, and `isRecording`. These are completely independent booleans, making invalid states (like `isStreaming === true` AND `isRecording === true`) technically possible. A unified state machine (e.g., Redux or XState) should be used.
