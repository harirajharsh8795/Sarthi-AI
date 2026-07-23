# ⚡ Saarthi AI — Edge Cognitive Offline RAG Assistant

![Track 2 RAG](https://img.shields.io/badge/Track-Track%202%20Intelligent%20Document%20Brain-blue)
![Hardware](https://img.shields.io/badge/Hardware-NVIDIA%20Jetson%20Orin%20Nano-76B900?logo=nvidia)
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
| **Banking** | 70+ Documents | RBI Master Directions, KYC Guidelines, Foreclosure Norms, Priority Sector Lending, Grievance Redressal |
| **Legal** | 15+ Documents | Bharatiya Nagarik Suraksha Sanhita (BNSS 2023), Bharatiya Nyaya Sanhita (BNS 2023), RTI Act 2005, Consumer Protection Act 2019, Motor Vehicles Act |
| **Medical** | 10+ Documents | National Health Mission (NHM) Standard Treatment Guidelines for Fever, Malaria, Dengue, TB, Typhoid, Hypertension, Diabetes & ICMR 2019 Clinical Guidelines |
| **Constitutional** | 2 Documents | Constitution of India (Complete English & Hindi Official Versions) |

**Total: 10,338+ chunks indexed. Hindi + English. Multilingual cross-lingual retrieval.**

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
User Query (Hindi / English / Hinglish)
           ↓
  Hinglish Glossary Expansion
  bukhar → fever, pyrexia, febrile
  177 colloquial term mappings
           ↓
  Multilingual Embedding Model
  (paraphrase-multilingual-mpnet-base-v2)
           ↓
  ┌─────────────────┬──────────────────────┐
  │   user_docs     │   knowledge_base     │
  │ (your uploads)  │ RBI, RTI, NHM, BNSS  │
  │ score ≥ 0.50   │ score ≥ 0.35         │
  └────────┬────────┴──────────┬───────────┘
           └────────┬──────────┘
             Tiered Merge + Domain Check
                     ↓
          Llama 3.2 1B via Ollama
          (temperature 0.1, grounded)
                     ↓
     Streaming Answer + Page Citations
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
- **Pre-download Models**: Ensure Whisper `tiny` and `paraphrase-multilingual-mpnet-base-v2` are pre-cached before your live demo slot to ensure 100% offline execution.
- **Speech Synthesis**: Install `espeak` (`sudo apt install -y espeak`) for `pyttsx3` Linux audio generation.
- **Network Access**: Access the web interface from any device on the same local network using `http://<JETSON_IP>:5173`.

---

## 🏆 Hackathon Details

- **Event**: EDGEMINDS Internship 2026
- **Track**: Track 2 — Intelligent Document Brain RAG
- **Hardware**: NVIDIA Jetson Orin Nano
- **Submission Date**: July 12, 2026
- **Demo Day**: July 14-15, 2026
