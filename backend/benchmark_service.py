import os
import time
import json
import logging
import psutil
from config import settings

logger = logging.getLogger("saarthi.benchmark")

class BenchmarkService:
    """
    Benchmarks system tasks (OCR, Embedding, Inference),
    maintains performance history, and supports automated stress testing.
    """
    
    def __init__(self):
        self.report_path = "benchmark_report.json"
        self.summary_path = "performance_summary.json"
        self.history_path = "benchmark_history.json"

    def record_run(self, pipeline_metrics: dict) -> dict:
        """
        Saves a pipeline run breakdown and compiles comparison indicators
        against historical runs.
        """
        # Load previous history
        history = []
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, "r") as f:
                    history = json.load(f)
            except Exception:
                pass
                
        # Calculate comparison indicators with the last run if available
        diffs = {}
        if history:
            prev = history[-1]
            for key, val in pipeline_metrics.items():
                if isinstance(val, (int, float)) and key in prev and isinstance(prev[key], (int, float)):
                    if prev[key] > 0:
                        pct_change = ((val - prev[key]) / prev[key]) * 100.0
                        diffs[key] = f"{pct_change:+.1f}%"
                    else:
                        diffs[key] = "0.0%"
        else:
            diffs = {k: "0.0%" for k in pipeline_metrics.keys() if isinstance(pipeline_metrics[k], (int, float))}

        run_record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metrics": pipeline_metrics,
            "comparison_vs_previous": diffs
        }
        
        # Append history
        history.append(run_record)
        # Cap history list size at 50
        history = history[-50:]
        
        try:
            with open(self.history_path, "w") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to write history: {e}")

        # Compile summaries
        summary = {
            "last_benchmark_timestamp": run_record["timestamp"],
            "current_run_latencies": pipeline_metrics,
            "performance_comparisons": diffs
        }
        
        try:
            with open(self.summary_path, "w") as f:
                json.dump(summary, f, indent=2)
            with open(self.report_path, "w") as f:
                json.dump(run_record, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to write reports: {e}")
            
        return run_record

    def run_stress_test(self, query_count: int = 50) -> dict:
        """
        Executes a rapid stress test suite simulating concurrent client queries
        and outputs stress statistics logs.
        """
        logger.info(f"Initiating stress test with {query_count} query executions...")
        start = time.perf_counter()
        
        success = 0
        failures = 0
        latencies = []
        
        # Mock RAG pipeline queries to gather timings
        for i in range(query_count):
            q_start = time.perf_counter()
            try:
                # Mock RAG query check
                time.sleep(0.01)  # simulated work
                success += 1
                latencies.append((time.perf_counter() - q_start) * 1000.0)
            except Exception:
                failures += 1
                
        duration = time.perf_counter() - start
        avg_lat = sum(latencies) / len(latencies) if latencies else 0.0
        p95_lat = sorted(latencies)[int(len(latencies)*0.95)] if latencies else 0.0
        
        stress_report = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_queries_run": query_count,
            "successful_queries": success,
            "failed_queries": failures,
            "stress_duration_seconds": round(duration, 3),
            "average_latency_ms": round(avg_lat, 2),
            "p95_latency_ms": round(p95_lat, 2)
        }
        
        logger.info(f"Stress test finished. Results: {stress_report}")
        return stress_report

benchmark_service = BenchmarkService()
