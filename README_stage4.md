# Stage 4B: Telemetry Dashboard + Voice (STT + TTS)

This stage adds a live system stats telemetry panel and integrates fully offline Speech-to-Text (Whisper base model) and Text-to-Speech (pyttsx3) audio interfaces.

## Prerequisites

1. **Ollama**: Ensure Ollama is running locally with the `llama3.2:1b` model pulled:
   ```bash
   ollama run llama3.2:1b
   ```
2. **Python Dependencies**:
   Install backend packages:
   ```bash
   pip install -r requirements_stage4.txt
   ```
   
   > [!IMPORTANT]
   > **Jetson / Linux PyTorch Warning**: On NVIDIA Jetson platforms running JetPack, PyTorch is pre-installed as a system package. To prevent overriding it with a non-CUDA pip package, install Whisper with `--no-deps`:
   > ```bash
   > pip install openai-whisper --no-deps
   > ```
   > Then manually install any remaining missing dependencies (e.g. `soundfile`, `pyttsx3`) without re-installing PyTorch.

3. **System Speech Backend (Linux/Jetson)**:
   `pyttsx3` on Linux/Ubuntu requires the `espeak` synthesizer system library. Run:
   ```bash
   sudo apt-get update && sudo apt-get install espeak -y
   ```

4. **Whisper Offline Model**:
   Whisper downloads the `base` model (~74MB) to `~/.cache/whisper/` on the first startup. It is highly recommended to run the app once while connected to download the model cache before deploying offline.

5. **Hindi Voice Pack (Optional)**:
   For Hindi speech synthesis, ensure a Hindi voice registry is installed on your OS (e.g., SAPI5 Hindi voice on Windows, or `espeak-hi` on Linux). If no Hindi voice is found, the system fallback is the default English voice.

6. **Node.js**: Verify that Node.js (version 18+) is installed.

---

## Running the Application

### Option A: Local Development (Separate Services)

1. **Start the FastAPI Backend**:
   Run the Uvicorn server in the root project directory:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   *The backend will run on `http://localhost:8000`. On first load, it will download the Whisper base model and load embedding structures.*

2. **Start the Vite Frontend**:
   Navigate to the `frontend` folder and launch the Vite dev server:
   ```bash
   cd frontend
   npm run dev
   ```
   *The React interface will run on `http://localhost:5173`.*

---

### Option B: Jetson Production Serving (Unified Single-Server)

If you compile a production bundle, FastAPI serves it automatically from the root url `/`:

1. **Build the React Frontend**:
   ```bash
   cd frontend
   npm run build
   ```
   This will output an optimized static single-page app to `./frontend/dist/`.

2. **Launch the FastAPI backend**:
   ```bash
   cd ..
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   Open your browser and navigate to `http://localhost:8000` to interact with the fully self-contained product.

---

## End-to-End Verification Flow

1. **Upload & Ingestion**: Upload a document and verify it indexes.
2. **System Stats Panel**:
   - In the left sidebar, click the collapsible **System stats** button.
   - Expand the panel to verify the 2x2 grid loads summary metrics (Avg Latency, Throughput t/s, Total Queries, Queries with Context).
   - Verify the scrollable table of the last 20 queries auto-refreshes every 10 seconds.
3. **Voice Input (STT)**:
   - Click the **Microphone** icon next to the chat text input.
   - Speak your query (Hindi or English).
   - Click the microphone icon again to stop recording.
   - Verify the text input box is populated with your spoken query transcript (allowing you to review/edit before sending).
4. **Voice Output (TTS)**:
   - Send the query and wait for the response to finish streaming.
   - Locate the **Speaker** icon in the top-right corner of the assistant's message bubble.
   - Click the speaker icon to play the synthesized audio stream.
   - Click the icon again during playback to stop speaking.
