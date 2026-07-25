# 🚀 NVIDIA Jetson Cloud Lab Deployment Guide (EdgeMinds 2026)

> **Booked Session**: APEX Tier — NVIDIA Jetson Nano  
> **Platform**: `edgeai.aiproff.ai`  
> **Slot Time**: July 25, 2026 @ 10:00 PM – 01:00 AM (3-Hour Access)  
> **Target Hardware**: NVIDIA Jetson Nano / Orin (ARM64 Edge Device)

---

## 📋 Step-by-Step Deployment Guide for Your Booked Slot

### Step 1: Open the Jetson Web Terminal
1. Go to `https://edgeai.aiproff.ai/dashboard`.
2. Find your active **APEX Tier - NVIDIA Jetson Nano 1** booking.
3. Click **"Open Terminal"** (or **"Early Access Available"**). This opens a web-based SSH shell connected directly to the Jetson board.

---

### Step 2: Clone / Sync Your GitHub Repository
In the Jetson Web Terminal, run:

```bash
# Clone repository (First time)
git clone https://github.com/harirajharsh8795/Sarthi-AI.git
cd Sarthi-AI

# If already cloned, pull latest changes:
git pull origin main
```

---

### Step 3: Run the Automated One-Command Jetson Setup
We have created an automated setup script that configures everything on the Jetson board automatically:

```bash
chmod +x scripts/jetson_setup.sh
./scripts/jetson_setup.sh
```

**What this script does automatically**:
- Installs `espeak`, `ffmpeg`, `tesseract-ocr` system packages.
- Configures environment for Jetson container Ollama network (`http://172.17.0.1:11434/api/generate`).
- Verifies model `llama3.2:1b` (pre-loaded on board).
- Verifies Knowledge Base vector index (2,714 chunks).
- Runs post-deployment health check (`python backend/health_check.py`).

---

### Step 4: Launch Backend & Frontend Servers

#### 1. Start Backend Server:
```bash
python backend/main.py
```
*Backend starts on `http://0.0.0.0:8000`.*

#### 2. Start Frontend UI (In a second terminal tab or background):
```bash
cd frontend
npm run dev -- --host
```
*Frontend starts on `http://0.0.0.0:5173`.*

---

### 🌐 Accessing the Live App During Your Demo
You can access the live application directly from your laptop browser using the Jetson IP or host URL provided on your dashboard:

- **Frontend UI**: `http://<JETSON_IP>:5173`
- **Backend API**: `http://<JETSON_IP>:8000`
- **API Docs (Swagger)**: `http://<JETSON_IP>:8000/docs`

---

## ⚙️ Automated CI/CD Pipelines

Our GitHub repository features 7 automated GitHub Actions CI/CD workflows:

1. **`jetson-ci.yml`**: Jetson Nano & ARM64 Edge Compatibility Validation.
2. **`backend.yml`**: Python FastAPI unit tests & security checks.
3. **`frontend.yml`**: Vite React production build verification.
4. **`docker.yml`**: Multi-arch Docker image build & push.
5. **`deploy.yml`**: Pre-deployment timestamp backup & zero-downtime reloads.
6. **`security.yml`**: Bandit, Safety dependency audit, & Secret scanner.
7. **`rag-ingestion.yml`**: Vector DB index validation & metadata checks.

Every `git push origin main` automatically triggers all 7 pipelines!
