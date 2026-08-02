#!/bin/bash
# ============================================================
#  SAARTHI AI — ONE-COMMAND PRODUCTION DEPLOYMENT
#  Usage: bash ~/Sarthi-AI/deploy.sh
# ============================================================
set -e

echo ""
echo "======================================================="
echo "  🚀 SAARTHI AI — DEPLOYMENT STARTING"
echo "======================================================="

# 1. Kill ALL old processes
echo "[1/6] Killing old processes..."
pkill -9 -f uvicorn 2>/dev/null || true
pkill -9 -f "python3 start" 2>/dev/null || true
pkill -9 -f "npm run dev" 2>/dev/null || true
pkill -9 -f node 2>/dev/null || true
pkill -9 -f ngrok 2>/dev/null || true
pkill -9 -f cloudflared 2>/dev/null || true
sleep 2

# 2. Pull latest code
echo "[2/6] Pulling latest code from GitHub..."
cd ~/Sarthi-AI
git pull origin chore/saarthi-ai-updates-20260731 || true

# 3. Build production frontend (skip if dist/ already exists to avoid OOM on Jetson)
if [ -d ~/Sarthi-AI/frontend/dist ]; then
    echo "[3/6] Frontend dist/ already exists — skipping build (saves RAM)."
else
    echo "[3/6] Building production frontend (this may take a minute)..."
    cd ~/Sarthi-AI/frontend
    npm run build
    cd ~/Sarthi-AI
fi

# 4. Start backend server (serves both API + static frontend on port 8000)
echo "[4/6] Starting FastAPI server on port 8000..."
nohup python3 start.py > server.log 2>&1 &
SERVER_PID=$!
echo "  Server PID: $SERVER_PID"

# 5. Wait for server to be FULLY healthy (with timeout)
echo "[5/6] Waiting for server health check (up to 60s)..."
HEALTHY=0
for i in $(seq 1 60); do
    if curl -sf http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
        echo "  ✅ Server HEALTHY after ${i} seconds"
        HEALTHY=1
        break
    fi
    # Check if server process died
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo "  ❌ Server process died! Check server.log:"
        tail -20 ~/Sarthi-AI/server.log
        exit 1
    fi
    sleep 1
done

if [ "$HEALTHY" -eq 0 ]; then
    echo "  ❌ Server failed to become healthy in 60s. Last log lines:"
    tail -20 ~/Sarthi-AI/server.log
    exit 1
fi

# 6. Start Ngrok tunnel pointing to port 8000
echo "[6/6] Starting Ngrok tunnel..."
cd ~
nohup ./ngrok http 8000 > ngrok.log 2>&1 &
sleep 4

# Extract and display the public URL
NGROK_URL=$(curl -sf http://127.0.0.1:4040/api/tunnels 2>/dev/null | grep -o 'https://[a-zA-Z0-9-]*\.ngrok-free\.app' | head -1)

echo ""
echo "======================================================="
if [ -n "$NGROK_URL" ]; then
    echo "  🎉 SAARTHI AI IS LIVE!"
    echo ""
    echo "  👉 $NGROK_URL"
else
    echo "  ⚠️  Ngrok URL not found. Try manually:"
    echo "  curl -s http://127.0.0.1:4040/api/tunnels | grep ngrok"
fi
echo ""
echo "  Server PID: $SERVER_PID"
echo "  Server Log: ~/Sarthi-AI/server.log"
echo "======================================================="
