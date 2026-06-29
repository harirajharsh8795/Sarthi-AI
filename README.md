# Saarthi AI — Edge-Optimized Offline Conversational Assistant

Saarthi AI is a fully offline, high-performance Retrieval-Augmented Generation (RAG) platform optimized for NVIDIA Jetson and edge deployments. Built specifically for sensitive domains (Medical, Legal, and Banking), it provides reliable, privacy-first answers without requiring internet connectivity.

---

## 🚀 Key Features

* **Offline-First RAG**: Complete search and generation workflows run entirely on local edge hardware using local embedding models and optimized local LLMs (`llama3.2:1b` via Ollama).
* **NVIDIA Jetson Optimization**: Automatic edge profiling (Power Saver, Balanced, Performance, Demo), swap tuning, worker count adjustments, and hardware-specific model warmups.
* **Security & Prompt Injection Protection**: Dual-stage sanitization (Prompt Guard) targeting Context Override, Instruction Hijacking, and Ignore-Previous-Instructions attacks.
* **Privacy Engine**: On-the-fly masking of sensitive Indian citizen identifiers (Aadhaar, PAN, Bank Accounts, Phone, and Emails) before logging or telemetry storage.
* **Multilingual Input & OCR**: Tesseract-based multi-language OCR sanitization and local Whisper/TTS hooks for voice interactions.

---

## 🛠️ Tech Stack
* **Frontend**: React, Vite, Framer Motion, Tailwind CSS, Lucide Icons
* **Backend**: FastAPI, SQLite, ChromaDB, Ollama
* **Testing**: Pytest, Pytest-Asyncio

---

## ⚙️ How to Run

### 1. Prerequisites
* Install [Ollama](https://ollama.com/) and pull the target model:
  ```bash
  ollama pull llama3.2:1b
  ```
* Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (ensure it is added to your system PATH).

### 2. Backend Server
* Install dependencies and run FastAPI server:
  ```bash
  pip install -r requirements.txt
  uvicorn main:app --host 0.0.0.0 --port 8000
  ```

### 3. Frontend Dev Server
* Navigate to the frontend directory, install dependencies, and run:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

### 4. Running Tests
* Run unit tests and security validation suite:
  ```bash
  pytest "test scripts (do not deploy to Jetson)/test_security.py"
  ```
