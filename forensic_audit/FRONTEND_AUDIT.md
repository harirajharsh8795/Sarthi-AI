# FRONTEND AUDIT

## Discovered Issues
1. **Duplicate Components:** `MessageBubble.jsx` exists in both `frontend/src/components/` and `frontend/src/components/chat/`. 
   - *Severity:* MEDIUM. Causes developer confusion and potential conflicting imports.
2. **Race Condition in SSE Switching:** 
   - *Severity:* HIGH. Switching conversations rapidly while SSE is streaming causes the `eventSource.onmessage` handler to append tokens to the *new* conversation's state because React state closures capture the old `activeConvId` but update the global `messages` array.
3. **Memory Leaks:** 
   - *Severity:* MEDIUM. `MediaRecorder` in `InputArea.jsx` / `ChatWorkspace.jsx` may not be properly cleaned up if the component unmounts during a recording.
4. **Prop Drilling:**
   - *Severity:* LOW. `ChatWorkspace.jsx` passes over 15 props down to `InputArea.jsx` and `ChatMessages.jsx`. A Context provider (e.g., `ChatContext`) should be introduced.
5. **Frozen UI (Resolved):**
   - *Severity:* CRITICAL (Previously). Uploading files originally disabled the entire `textarea`, freezing the UI.
