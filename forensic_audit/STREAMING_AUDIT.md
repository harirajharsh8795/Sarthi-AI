# STREAMING ENGINE AUDIT

## Pipeline Flaws
1. **EventSource Reconnection:**
   - *Severity:* HIGH. The standard `EventSource` API in JS automatically attempts to reconnect on drop. The backend `/api/stream` endpoint treats a reconnect as a *new* query and will re-run the entire LLM generation, leading to duplicated responses.
2. **In-Flight Cancellation:**
   - *Severity:* MEDIUM. Clicking "Stop Generating" closes the frontend `EventSource`, but there is no mechanism to propagate an `AbortSignal` to the backend LLM thread to stop token generation.
