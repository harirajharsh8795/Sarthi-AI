#!/bin/bash
# ============================================================
#  SAARTHI AI — MASTER ONE-COMMAND DEPLOYMENT
#  Usage: bash ~/Sarthi-AI/deploy.sh
#  Handles: Cleanup → Code Pull → Ollama Verify → Frontend Build
#           → Backend Start → Health Check → Ngrok Tunnel
# ============================================================
set -e

echo ""
echo "======================================================="
echo "  🚀 SAARTHI AI — MASTER DEPLOYMENT STARTING"
echo "======================================================="
echo ""

# ─── 1. KILL ALL OLD PROCESSES ──────────────────────────────
echo "[1/8] Killing old processes..."
pkill -9 -f uvicorn 2>/dev/null || true
pkill -9 -f "python3 start" 2>/dev/null || true
pkill -9 -f "npm run dev" 2>/dev/null || true
pkill -9 -f node 2>/dev/null || true
pkill -9 -f ngrok 2>/dev/null || true
pkill -9 -f cloudflared 2>/dev/null || true
sleep 2
echo "  ✅ Old processes killed."

# ─── 2. PULL LATEST CODE ────────────────────────────────────
echo "[2/8] Pulling latest code from GitHub..."
cd ~/Sarthi-AI
git pull origin chore/saarthi-ai-updates-20260731 || true
echo "  ✅ Code updated."

# ─── 3. VERIFY OLLAMA IS RUNNING & MODEL IS AVAILABLE ───────
echo "[3/8] Verifying Ollama service and LLM model..."

OLLAMA_HOST=""
for host in "localhost" "127.0.0.1" "172.17.0.1"; do
    if curl -sf "http://${host}:11434/api/tags" > /dev/null 2>&1; then
        OLLAMA_HOST="http://${host}:11434"
        echo "  ✅ Ollama found at: $OLLAMA_HOST"
        break
    fi
done

if [ -z "$OLLAMA_HOST" ]; then
    echo "  ❌ Ollama service not found on any host!"
    echo "  Try: curl http://172.17.0.1:11434/api/tags"
    exit 1
fi

# Check if llama3.2:1b model is available
MODEL_EXISTS=$(curl -sf "${OLLAMA_HOST}/api/tags" 2>/dev/null | grep -c "llama3.2:1b" || true)
if [ "$MODEL_EXISTS" -eq 0 ]; then
    echo "  ⚠️  Model llama3.2:1b not found. Pulling..."
    curl -sf -X POST "${OLLAMA_HOST}/api/pull" -d '{"name":"llama3.2:1b","stream":false}' --max-time 300 || true
    echo "  ✅ Model pulled."
else
    echo "  ✅ Model llama3.2:1b is available."
fi

# ─── 4. PRE-WARM OLLAMA MODEL (CRITICAL: eliminates cold-start latency) ──
echo "[4/8] Pre-warming LLM model into GPU memory (keep_alive=60m)..."
WARMUP_RESULT=$(curl -sf -X POST "${OLLAMA_HOST}/api/generate" \
    -d '{"model":"llama3.2:1b","prompt":"Summarize: Right to Information Act 2005 empowers Indian citizens. Answer:","stream":false,"keep_alive":"60m"}' \
    --max-time 60 2>/dev/null || echo "FAIL")

if echo "$WARMUP_RESULT" | grep -q "response"; then
    echo "  ✅ Model warmed up and loaded into GPU memory!"
else
    echo "  ⚠️  Model warmup returned unexpected result. Continuing..."
    echo "  Response: ${WARMUP_RESULT:0:100}"
fi

# ─── 5. BUILD LATEST FRONTEND BUNDLE ─────────────────────────
echo "[5/8] Building production frontend..."
cd ~/Sarthi-AI/frontend

# Install deps if missing
if [ ! -d node_modules ]; then
    echo "  Installing npm dependencies..."
    npm install --production=false 2>&1 | tail -3
fi

# Build with reduced memory usage
NODE_OPTIONS="--max-old-space-size=512" npm run build 2>&1 | tail -5

if [ -f dist/index.html ]; then
    echo "  ✅ Frontend built successfully."
else
    echo "  ❌ Frontend build failed! Check errors above."
    exit 1
fi
cd ~/Sarthi-AI

# ─── 6. START BACKEND SERVER ────────────────────────────────
echo "[6/8] Starting FastAPI server on port 8000..."
cd ~/Sarthi-AI
nohup python3 start.py > server.log 2>&1 &
SERVER_PID=$!
echo "  Server PID: $SERVER_PID"

# ─── 7. WAIT FOR SERVER HEALTH CHECK ────────────────────────
echo "[7/8] Waiting for server health check (up to 90s)..."
HEALTHY=0
for i in $(seq 1 90); do
    if curl -sf http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
        echo "  ✅ Server HEALTHY after ${i} seconds"
        HEALTHY=1
        break
    fi
    # Check if server process died
    if ! kill -0 $SERVER_PID 2>/dev/null; then
        echo "  ❌ Server process died! Last 30 lines of server.log:"
        tail -30 ~/Sarthi-AI/server.log
        exit 1
    fi
    sleep 1
done

if [ "$HEALTHY" -eq 0 ]; then
    echo "  ❌ Server failed to become healthy in 90s. Last log lines:"
    tail -30 ~/Sarthi-AI/server.log
    exit 1
fi

# Quick API verification
echo "  Verifying API endpoints..."
API_TEST=$(curl -sf http://127.0.0.1:8000/api/health 2>/dev/null || echo "FAIL")
if echo "$API_TEST" | grep -qi "ok\|healthy\|status"; then
    echo "  ✅ API endpoints responding correctly."
else
    echo "  ⚠️  API health response: ${API_TEST:0:100}"
fi

# ─── 8. START NGROK TUNNEL ──────────────────────────────────
echo "[8/8] Starting Ngrok tunnel..."
cd ~
nohup ./ngrok http 8000 > ngrok.log 2>&1 &
sleep 5

# Extract and display the public URL
NGROK_URL=$(curl -sf http://127.0.0.1:4040/api/tunnels 2>/dev/null | grep -o 'https://[a-zA-Z0-9-]*\.ngrok-free\.app' | head -1)

echo ""
echo "======================================================="
if [ -n "$NGROK_URL" ]; then
    echo "  🎉 SAARTHI AI IS LIVE!"
    echo ""
    echo "  👉 PUBLIC URL: $NGROK_URL"
    echo ""
    echo "  📋 Quick Test Commands:"
    echo "     curl $NGROK_URL/api/health"
    echo ""
else
    echo "  ⚠️  Ngrok URL not found yet. Try manually:"
    echo "  curl -s http://127.0.0.1:4040/api/tunnels | grep ngrok"
fi
echo ""
echo "  Server PID: $SERVER_PID"
echo "  Server Log: tail -f ~/Sarthi-AI/server.log"
echo "  Ollama:     $OLLAMA_HOST"
echo "======================================================="
