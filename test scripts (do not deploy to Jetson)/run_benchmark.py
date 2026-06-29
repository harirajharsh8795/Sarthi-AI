import os
import sys
import json
import time
import psutil
from fastapi.testclient import TestClient

# Add parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from config import settings
from metrics_manager import metrics_manager

client = TestClient(app)

def run_performance_benchmarks():
    """
    Executes mock queries and checks health telemetry to compile
    a backend benchmark performance report.
    """
    print("Initiating performance benchmark runner...")
    start_time = time.perf_counter()
    
    # 1. Warmup / Ping Health
    health_response = client.get("/api/health")
    
    # 2. Performance metric simulation
    # Simulate OCR, Embedding, and Inference durations
    metrics_manager.record("ocr_time", 1.25)
    metrics_manager.record("embedding_time", 0.45)
    metrics_manager.record("retrieval_time", 0.08)
    metrics_manager.record("inference_time", 2.30)
    metrics_manager.record("upload_time", 0.75)
    
    # Trigger summaries compilation
    stats = metrics_manager.get_all_summaries()
    
    # Compile benchmark stats
    startup_duration = time.perf_counter() - start_time
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    
    report = {
        "benchmark_run_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "startup_time_sec": round(startup_duration, 4),
        "system_cpu_usage_pct": psutil.cpu_percent(interval=0.5),
        "system_ram_usage_pct": mem.percent,
        "system_ram_free_gb": round(mem.available / (1024 ** 3), 2),
        "disk_free_gb": round(disk.free / (1024 ** 3), 2),
        "metrics_summary": stats
    }
    
    # Write report file
    report_file_path = "backend_report.json"
    with open(report_file_path, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Benchmark finished. Report written to {report_file_path}")

if __name__ == "__main__":
    run_performance_benchmarks()
