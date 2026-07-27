#!/bin/bash
# ==============================================================================
# Saarthi AI — One-Command Automated Setup Script for NVIDIA Jetson Cloud Lab
# Hackathon: EdgeMinds 2026 (APEX Tier - Jetson Nano / Orin)
# ==============================================================================

set -e

echo "🚀 Starting Saarthi AI Jetson Nano Setup..."

# 1. System Package Installation (Non-blocking if non-root)
echo "📦 Checking system dependencies..."
sudo -n apt-get update -qq 2>/dev/null || true
sudo -n apt-get install -y -qq espeak ffmpeg tesseract-ocr tesseract-ocr-hin portaudio19-dev python3-pyaudio 2>/dev/null || true

# 2. Configure Environment Variables for Jetson Ollama Container
echo "⚙️ Configuring Environment Variables..."
export SAARTHI_OLLAMA_URL="http://172.17.0.1:11434/api/generate"
export SAARTHI_LLM_MODEL="llama3.2:1b"
export OMP_NUM_THREADS=4

# 3. Install Python Dependencies (preserving JetPack PyTorch)
echo "🐍 Installing Python Dependencies..."
pip install -r requirements.txt --quiet || pip install -r requirements.txt --no-deps

# 4. Verify Local Ollama Connectivity
echo "🔍 Testing Ollama REST API Connectivity on Jetson Network..."
curl -s -X POST http://172.17.0.1:11434/api/generate -d '{"model":"llama3.2:1b","prompt":"test","stream":false}' > /dev/null && echo "✅ Ollama API Connected!" || echo "⚠️ Local Ollama warning: Ensure Ollama daemon is running."

# 5. Pre-Seed Knowledge Base Index
echo "🌱 Verifying Knowledge Base Index..."
python seed_knowledge_base.py

# 6. Run Post-Deployment Health Check
echo "🩺 Running Health Check..."
python backend/health_check.py

echo ""
echo "=============================================================================="
echo "🎉 SAARTHI AI JETSON SETUP COMPLETE!"
echo "To start the Backend Server, run:"
echo "   python backend/main.py"
echo ""
echo "To start the Frontend UI (if Node.js is installed), run:"
echo "   cd frontend && npm install && npm run dev -- --host"
echo "=============================================================================="
