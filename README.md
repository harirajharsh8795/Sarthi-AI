# ⚡ Saarthi AI — Edge Cognitive Offline RAG Assistant

![Architecture](https://img.shields.io/badge/Architecture-Hybrid%20RAG-blue)
![Hardware](https://img.shields.io/badge/Hardware-NVIDIA%20Jetson%20Orin-76B900?logo=nvidia)
![Model](https://img.shields.io/badge/SLM-Llama%203.2%201B-purple)
![Offline](https://img.shields.io/badge/Deployment-100%25%20Offline%20First-success)
![Backend](https://img.shields.io/badge/Backend-Python%20FastAPI-009688?logo=fastapi)
![Frontend](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB?logo=react)

> **Privacy-first, offline RAG assistant for Indian citizens — answers Legal, Banking, and Medical questions with page-level citations, running entirely on NVIDIA Jetson with zero internet dependency.**

---

## 🎯 Why Saarthi AI?

| Problem | Solution |
|---|---|
| **Complex Regulations**: Citizens struggle to comprehend complex RBI circulars, legal acts, and medical guidelines. | **Simple Hindi/English Answers**: Translates dense legal/banking jargon into plain, actionable advice with exact page citations. |
| **Data Privacy & Leakage**: Uploading confidential financial or medical reports to cloud AI creates data leakage risks. | **100% On-Device Processing**: Runs fully locally on NVIDIA Jetson with zero external API calls or telemetry leaks. |
| **Connectivity Barriers**: Rural healthcare centers and remote administrative areas lack continuous internet connectivity. | **100% Offline-First Architecture**: Functions completely offline after initial one-time model setup. |
| **AI Hallucinations**: General-purpose LLMs hallucinate medical diagnoses and outdated legal penalties. | **Honest Grounded Fallback**: Enforces strict grounding with red confidence indicators whenever source data is insufficient. |

---

## 📚 Knowledge Base

| Domain | Document Count | Key Sources & Coverage |
|---|---|---|
| **Banking** | **97 Documents** | RBI Master Directions, KYC Guidelines, Foreclosure Norms, Priority Sector Lending, Grievance Redressal, Loan Guidelines |
| **Legal** | **112 Documents** | Bharatiya Nagarik Suraksha Sanhita (BNSS 2023), Bharatiya Nyaya Sanhita (BNS 2023), Bharatiya Sakshya Adhiniyam (BSA 2023), RTI Act 2005, Consumer Protection Act 2019, Motor Vehicles Act, Labour Laws |
| **Medical** | **129 Documents** | National Health Mission (NHM) Standard Treatment Guidelines for Fever, Malaria, Dengue, TB, Typhoid, Diabetes, Hypertension, Cardiac, Chronic, Mental Health, Sexual Health & ICMR Guidelines |
| **Common & Constitutional** | **15 Documents** | Ayushman Bharat PM-JAY, PM-Kisan, Cyber Safety Guidelines, Constitution of India (Complete English & Hindi Official Versions) |

**Total: 353 documents (2,714 chunks indexed). Hindi + English. Multilingual cross-lingual retrieval.**

---

## ✨ Key Features

- **Hybrid RAG Pipeline**: Simultaneously queries user-uploaded private documents AND the pre-seeded sovereign Knowledge Base.
- **Bilingual Support (Hindi & English)**: Seamlessly accepts and responds in both Hindi (Devanagari) and English.
- **177 Hinglish Term Mappings**: Built-in colloquial dictionary (`bukhar` → `fever`, `BP high hai` → `hypertension`).
- **Page-Level Exact Citations**: Every claim is linked back to the exact source document and page number (`[Page X]`).
- **Session Isolation**: User-uploaded documents are cryptographically isolated to the active session and never leaked across users.
- **Persistent Conversation History**: Full multi-turn session persistence stored locally via SQLite.
- **Offline Speech-to-Text (STT)**: Voice input powered by OpenAI Whisper (`tiny` model) running fully on-device.
- **Offline Text-to-Speech (TTS)**: Voice responses powered by `pyttsx3` with `espeak` fallback.
- **Multi-Format Document Upload**: Accepts PDF, DOCX, JPG, PNG, WEBP files with automatic Tesseract OCR fallback for scanned images.
- **Privacy-First Zero Internet**: Inference runs 100% offline with automatic deletion of temporary raw ingestion files.
- **Live Telemetry & Observability**: Real-time dashboard rendering tokens/sec throughput, TTFT latency, and memory consumption.
- **Dark Mode & Light Mode UI**: Premium modern glassmorphism design system.
- **Hindi & English UI Toggle**: On-the-fly language switching across the entire interface.
- **Honest Fallback & Red Indicator**: Displays a red warning badge when retrieved evidence is weak, refusing to guess medical dosages.
- **Dual-Stage Prompt Guard**: Filters prompt injection attempts, SQL injection, XSS, and path traversal patterns.
- **PII Privacy Engine**: Auto-masks sensitive numbers (Aadhaar, PAN, Bank Account numbers) prior to logging.

---

## 🏗️ System Architecture

```text
               ┌─────────────────────────────────────────────────────────┐
               │           User Interface (React 18 + Vite)              │
               │      Voice Input (STT)  │  Text Input (Hindi/English)   │
               └────────────────────────────┬────────────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │              FastAPI Backend Gateway                    │
               │   • Prompt Guard Security  • PII Anonymization Engine   │
               └────────────────────────────┬────────────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │             Query Enhancement Subsystem                 │
               │   • 177 Hinglish Dictionary Expansion (bukhar → fever)  │
               │   • Contextual Query Rewriter & Intent Routing          │
               └────────────────────────────┬────────────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │         Multilingual Sentence Embedding Engine          │
               │       (paraphrase-multilingual-mpnet-base-v2)           │
               └────────────────────────────┬────────────────────────────┘
                                            │
                      ┌─────────────────────┴─────────────────────┐
                      ▼                                           ▼
       ┌─────────────────────────────┐             ┌─────────────────────────────┐
       │   user_docs Vector Index    │             │   saarthi_kb Vector Index   │
       │   (Session-Isolated Uploads)│             │ (353 Sovereign KB Documents)│
       │     Threshold: score ≥ 0.50 │             │    Threshold: score ≥ 0.35  │
       └──────────────┬──────────────┘             └──────────────┬──────────────┘
                      └─────────────────────┬─────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │           Context Processing & Reranking                │
               │   • Tiered Context Merge   • Relevance Reranker         │
               │   • Context Compression    • Grounding Verification     │
               └────────────────────────────┬────────────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │              Local SLM Generation Engine                │
               │       Llama 3.2 1B via Ollama API (num_ctx: 1024)       │
               └────────────────────────────┬────────────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │           Post-Processing & Output Pipeline             │
               │   • Citation Mapper        • Layout Formatting          │
               │   • Grounding Confidence   • Speech Output (TTS)        │
               └────────────────────────────┬────────────────────────────┘
                                            │
                                            ▼
               ┌─────────────────────────────────────────────────────────┐
               │            Streamed Response to End User                │
               └─────────────────────────────────────────────────────────┘
```

---

## 🧪 Demo Queries

```text
Query 1: "KYC verification process kya hai?"
→ Expect: Detailed step-by-step answer citing RBI Master Direction with exact page numbers, green confidence dot.

Query 2: "Consumer complaint kaise file karein?"
→ Expect: Official procedure under Consumer Protection Act 2019 with step-by-step guidance, green confidence dot.

Query 3: Upload any private PDF then ask "Is document ka summary do"
→ Expect: Structured summary generated directly from your uploaded file, cited with your document filename.

Query 4: "Mujhe bukhar hai, kya dawai leni chahiye?"
→ Expect: Red confidence dot indicator, honest disclaimer recommending medical consultation, zero dangerous drug prescriptions.
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React 18 + Vite + Tailwind CSS + Framer Motion |
| **Backend** | Python 3.10+ FastAPI + Uvicorn |
| **SLM Inference Engine** | Llama 3.2 1B via local Ollama API (`num_ctx: 1024`) |
| **Embedding Model** | `sentence-transformers/paraphrase-multilingual-mpnet-base-v2` |
| **Vector Database** | ChromaDB (Local Persistent Storage) |
| **Metadata Database** | SQLite (WAL Mode enabled) |
| **OCR Engine** | Tesseract OCR (`eng` + `hin`) with image binarization |
| **Speech-to-Text (STT)** | OpenAI Whisper `tiny` (Offline) |
| **Text-to-Speech (TTS)** | `pyttsx3` with `espeak` Linux backend (Offline) |
| **Target Hardware** | NVIDIA Jetson Orin Nano / Orin AGX |

---

## 🚀 Quick Start Guide

### Prerequisites
Install [Ollama](https://ollama.com) and pull the approved 1B SLM model:
```bash
ollama pull llama3.2:1b
```

Install system dependencies (Linux/Ubuntu):
```bash
sudo apt-get update
sudo apt-get install -y espeak ffmpeg tesseract-ocr tesseract-ocr-hin
```

### Installation & Setup

1. **Clone the Repository**:
```bash
git clone https://github.com/harirajharsh8795/Sarthi-AI.git
cd Sarthi-AI
```

2. **Install Python Dependencies**:
```bash
pip install -r requirements.txt
```

3. **One-Time Knowledge Base Seeding**:
```bash
python seed_knowledge_base.py
```

4. **Start Backend Server**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

5. **Build and Run Frontend**:
```bash
cd frontend
npm install
npm run build
npm run dev
```

---

## 📌 NVIDIA Jetson Orin Deployment Notes

- **PyTorch Preservation**: On Jetson JetPack environment, install OpenAI Whisper with `--no-deps` flag (`pip install openai-whisper --no-deps`) to prevent pip from overwriting JetPack-optimized PyTorch binaries.
- **Pre-download Models**: Ensure Whisper `tiny` and `paraphrase-multilingual-mpnet-base-v2` are pre-cached before your live demo to ensure 100% offline execution.
- **Speech Synthesis**: Install `espeak` (`sudo apt install -y espeak`) for `pyttsx3` Linux audio generation.
- **Network Access**: Access the web interface from any device on the same local network using `http://<JETSON_IP>:5173`.
