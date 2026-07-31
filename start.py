#!/usr/bin/env python3
"""
Saarthi AI — One-Command Full Stack Launcher
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ek command se poora system start hota hai:
  1. FastAPI backend → http://localhost:8000
  2. Vite React frontend → http://localhost:5173
  3. Browser automatically khulta hai

Usage:
    python start.py

Ya Windows PowerShell mein:
    python start.py
"""

import os
import sys

# 1. Root directory set karo
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

# 2. Backend ko Python path mein add karo
sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

# Reconfigure stdout/stderr for UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# 3. Banner print karo
print("\n" + "=" * 55)
print("  SAARTHI AI — FULL STACK LAUNCHER")
print("=" * 55)
print("  Backend API  →  http://localhost:8000")
print("  Frontend UI  →  http://localhost:5173")
print("  API Docs     →  http://localhost:8000/docs")
print("=" * 55 + "\n")


# 4. Uvicorn se backend start karo — main.py ka lifespan
#    automatically frontend ko bhi start kar deta hai
try:
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
except ImportError:
    print("❌ uvicorn not found. Run: pip install uvicorn")
    sys.exit(1)
except Exception as e:
    print(f"❌ Startup error: {e}")
    sys.exit(1)
