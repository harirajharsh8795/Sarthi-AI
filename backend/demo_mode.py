import os
import json
import time
import logging
from config import settings
from edge_runtime import edge_runtime_optimizer
from resource_monitor import resource_monitor
from model_manager import model_lifecycle_manager
from offline_engine import offline_engine
from cache_manager import cache_manager
from benchmark_service import benchmark_service
from deployment_validator import deployment_validator
from diagnostics import system_diagnostics
from edge_score import edge_performance_scorecard

logger = logging.getLogger("saarthi.demo")

class HackathonDemoMode:
    """
    Provides a single command entry point to trigger diagnostic tests
    and compile all dashboard metadata files for pitch slide decks.
    """
    
    def execute_demo_suite(self) -> dict:
        print("Starting Saarthi AI demo check suite...")
        
        # 1. Warmup model
        model_lifecycle_manager.warmup_model()
        
        # 2. Run system checks
        deploy_res = deployment_validator.validate_deployment()
        off_res = offline_engine.check_offline_readiness()
        diag_res = system_diagnostics.diagnose_system()
        score_res = edge_performance_scorecard.calculate_readiness_score()
        
        # 3. Simulate a RAG pipeline run to trigger performance profiling
        sim_metrics = {
            "ocr_time_ms": 110.0,
            "embedding_time_ms": 75.0,
            "retrieval_time_ms": 32.0,
            "ranking_time_ms": 12.0,
            "inference_time_ms": 1780.0,
            "streaming_time_ms": 840.0,
            "total_response_time_ms": 2849.0
        }
        bench_res = benchmark_service.record_run(sim_metrics)
        
        # 4. Dump individual telemetry JSON files as requested
        try:
            with open("edge_score.json", "w") as f:
                json.dump(score_res, f, indent=2)
            with open("diagnostics.json", "w") as f:
                json.dump(diag_res, f, indent=2)
            print("Successfully dumped edge_score.json and diagnostics.json.")
        except Exception as e:
            logger.error(f"Failed to dump demo configurations: {e}")
            
        summary = {
            "demo_run_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "PASS" if score_res["edge_readiness_score"] >= 60 else "FAIL",
            "edge_readiness_score": score_res["edge_readiness_score"],
            "offline_score": off_res["offline_score"],
            "diagnostics": diag_res,
            "benchmark": bench_res
        }
        
        print("Demo suite checks complete. Ready for presentation.")
        return summary

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    demo = HackathonDemoMode()
    res = demo.execute_demo_suite()
    print(json.dumps(res, indent=2))
