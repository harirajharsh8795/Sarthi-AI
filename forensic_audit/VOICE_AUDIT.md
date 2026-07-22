# VOICE PIPELINE AUDIT

## Pipeline Flaws
1. **Audio Chunking:**
   - *Severity:* LOW. `MediaRecorder` captures audio in arbitrary timeslices. If the network drops during voice upload, the entire audio blob is lost. It should stream binary data over WebSockets instead.
2. **Whisper Bottleneck:**
   - *Severity:* MEDIUM. Voice transcription runs synchronously on the backend, blocking the main event loop if not dispatched to a `ThreadPoolExecutor`.
