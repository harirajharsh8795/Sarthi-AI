# Saarthi AI - Production Deployment Guide

This document provides step-by-step instructions for deploying **Saarthi AI** across Local Development, Docker Containers, Production Servers, and Jetson Orin Edge Devices.

---

## 1. Quick Start (Local Development)

```bash
# 1. Clone repository
git clone https://github.com/harirajharsh8795/Sarthi-AI.git
cd Saarthi-AI

# 2. Setup Python environment & install backend dependencies
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
pip install -r backend/requirements.txt

# 3. Setup Frontend dependencies
cd frontend
npm install
npm run build
cd ..

# 4. Run Migration & Health Check
python scripts/migrate_db.py
python backend/health_check.py

# 5. Launch Backend Service
python backend/main.py
```

---

## 2. Docker Production Deployment

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Build & Launch Containers
docker-compose -f docker-compose.prod.yml up --build -d

# 3. Verify Health Status
docker ps
python backend/health_check.py
```

---

## 3. Jetson Orin Edge Deployment

Refer to [JETSON_DEPLOYMENT.md](file:///e:/Desktop/Saarthi%20AI/JETSON_DEPLOYMENT.md) for full hardware acceleration & Ollama configuration details.
