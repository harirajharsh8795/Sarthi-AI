import os
import sys
import time
import psutil
import json
import urllib.request

def get_system_telemetry():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()
    ram_used_mb = memory.used / (1024 * 1024)
    ram_total_mb = memory.total / (1024 * 1024)
    ram_percent = memory.percent

    # Check GPU if NVIDIA NVML is available (e.g. Jetson Orin)
    gpu_percent = 0.0
    try:
        import pynvml
        pynvml.nvmlInit()
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        util = pynvml.nvmlDeviceGetUtilizationRates(handle)
        gpu_percent = float(util.gpu)
    except Exception:
        gpu_percent = 0.0

    # Check Ollama Status
    ollama_status = "OFFLINE"
    ollama_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434") + "/api/tags"
    try:
        req = urllib.request.Request(ollama_url)
        with urllib.request.urlopen(req, timeout=2) as res:
            if res.status == 200:
                ollama_status = "ONLINE"
    except Exception:
        ollama_status = "OFFLINE"

    telemetry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage_pct": cpu_percent,
        "ram_used_mb": round(ram_used_mb, 1),
        "ram_total_mb": round(ram_total_mb, 1),
        "ram_usage_pct": ram_percent,
        "gpu_usage_pct": gpu_percent,
        "ollama_status": ollama_status
    }
    return telemetry

if __name__ == "__main__":
    t = get_system_telemetry()
    print(json.dumps(t, indent=2))
