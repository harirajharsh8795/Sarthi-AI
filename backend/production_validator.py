import os
import json
import psutil
import shutil
import requests
from config import settings

class ProductionValidator:
    """
    Validates final production configurations, system dependencies,
    directories write rights, and outputs production_report.json.
    """
    
    def run_production_checks(self) -> dict:
        issues = []
        
        # 1. Check directories permissions
        write_ok = True
        test_dir = "./data/test_perm"
        try:
            os.makedirs(test_dir, exist_ok=True)
            test_file = os.path.join(test_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            os.rmdir(test_dir)
        except Exception:
            write_ok = False
            issues.append("DATA_DIR_NOT_WRITABLE")

        # 2. Check memory & swap configs
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        swap_configured = swap.total > 0
        
        # 3. Model loaded state
        model_ready = False
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1.0)
            if r.status_code == 200:
                models = [m["name"] for m in r.json().get("models", [])]
                if any(settings.LLM_MODEL_NAME in m or m in settings.LLM_MODEL_NAME for m in models):
                    model_ready = True
        except Exception:
            pass
            
        if not model_ready:
            issues.append("LLM_MODEL_MISSING")

        # Calculate score out of 100
        score = 100
        if issues:
            score -= len(issues) * 20
        if mem.percent > 90.0:
            score -= 10
            
        status = "PRODUCTION_READY" if score >= 80 else "WARNING"
        
        report = {
            "overall_production_score": max(0, score),
            "status": status,
            "checklist": {
                "write_permissions": "PASS" if write_ok else "FAIL",
                "swap_memory_enabled": "PASS" if swap_configured else "WARNING",
                "model_available": "PASS" if model_ready else "FAIL",
                "cpu_efficiency": "PASS" if psutil.cpu_percent() < 85.0 else "WARNING"
            },
            "identified_risks": issues
        }
        
        try:
            with open("production_report.json", "w") as f:
                json.dump(report, f, indent=2)
        except Exception:
            pass
            
        return report

production_validator = ProductionValidator()
