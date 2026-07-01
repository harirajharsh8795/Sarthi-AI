import logging
import psutil
from config import settings
from offline_engine import offline_engine
from recovery_service import recovery_service
from model_manager import model_lifecycle_manager
from deployment_validator import deployment_validator

logger = logging.getLogger("saarthi.score")

class EdgePerformanceScorecard:
    """
    Calculates Edge Readiness Score (0-100) combining offline capabilities,
    memory bounds, latencies, circuit breakers, and load status.
    """
    
    def calculate_readiness_score(self) -> dict:
        # 1. Offline capability score (25% weight)
        off_res = offline_engine.check_offline_readiness()
        off_score = off_res["offline_score"]

        # 2. Memory usage score (20% weight)
        mem = psutil.virtual_memory()
        # Scale score: 100 - memory_percent
        mem_score = 100.0 - mem.percent

        # 3. Model lifecycle state score (15% weight)
        model_status = model_lifecycle_manager.get_lifecycle_status()
        state = model_status["state"]
        if state == "warm":
            model_score = 100.0
        elif state == "warming":
            model_score = 75.0
        elif state == "cold":
            model_score = 50.0
        else:
            model_score = 25.0

        # 4. Fault Recovery status score (15% weight)
        rec_status = recovery_service.get_recovery_status()
        rec_score = 100.0
        # Deduct if circuit breakers are open
        if rec_status["db_circuit_breaker_state"] == "OPEN":
            rec_score -= 40
        if rec_status["ollama_circuit_breaker_state"] == "OPEN":
            rec_score -= 40
        # Deduct points per recent recovery failure event (max 20 points deduction)
        rec_score -= min(20, len(rec_status["recent_recovery_events"]) * 5)

        # 5. Deployment validation score (15% weight)
        val_res = deployment_validator.validate_deployment()
        val_status = val_res["status"]
        if val_status == "PASS":
            val_score = 100.0
        elif val_status == "WARNING":
            val_score = 70.0
        else:
            val_score = 30.0

        # 6. CPU load score (10% weight)
        cpu = psutil.cpu_percent()
        cpu_score = 100.0 - cpu

        # Compile final weighted scorecard
        final_score = (
            (off_score * 0.25) + 
            (mem_score * 0.20) + 
            (model_score * 0.15) + 
            (rec_score * 0.15) + 
            (val_score * 0.15) + 
            (cpu_score * 0.10)
        )
        
        score_val = round(max(0.0, min(100.0, final_score)), 2)
        
        if score_val >= 85:
            label = "Excellent Edge Readiness"
            reason = "Local components are functional and device resource levels are optimal."
        elif score_val >= 60:
            label = "Moderate Edge Readiness"
            reason = "System is operational, but memory pressures or warning checks are present."
        else:
            label = "Low Edge Readiness"
            reason = "Key services are unreachable, or system resource levels are critical."

        logger.info(f"Edge Readiness Scorecard: {score_val} ({label})")
        
        return {
            "edge_readiness_score": score_val,
            "readiness_label": label,
            "reason": reason,
            "components": {
                "offline_readiness_pct": off_score,
                "memory_efficiency_pct": round(mem_score, 1),
                "model_status_pct": model_score,
                "recovery_stability_pct": rec_score,
                "deployment_health_pct": val_score,
                "cpu_efficiency_pct": round(cpu_score, 1)
            }
        }

edge_performance_scorecard = EdgePerformanceScorecard()
