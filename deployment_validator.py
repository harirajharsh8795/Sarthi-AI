import os
import shutil
import json
import logging
import psutil
import requests
from config import settings

logger = logging.getLogger("saarthi.validator")

class DeploymentValidator:
    """
    Validates hardware and system dependencies before startup,
    flagging missing software packages or insufficient disk space.
    """
    
    def validate_deployment(self) -> dict:
        """
        Runs check routines for Tesseract, Whisper, Ollama, SQLite, and system parameters.
        Generates deployment_report.json.
        """
        issues = []
        status = "PASS"
        
        # 1. Tesseract OCR check
        tesseract_ok = bool(shutil.which("tesseract"))
        if not tesseract_ok:
            # Check Winget paths
            user_profile = os.environ.get("USERPROFILE", "")
            tess_path = os.path.join(user_profile, "AppData", "Local", "Tesseract-OCR", "tesseract.exe")
            if os.path.exists(tess_path):
                tesseract_ok = True
                
        if not tesseract_ok:
            status = "WARNING"
            issues.append("Tesseract OCR is not found on path. OCR uploads will fail.")

        # 2. Ollama connection
        ollama_ok = False
        model_ok = False
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1.0)
            if r.status_code == 200:
                ollama_ok = True
                models = [m["name"] for m in r.json().get("models", [])]
                if any(settings.LLM_MODEL_NAME in m or m in settings.LLM_MODEL_NAME for m in models):
                    model_ok = True
        except Exception:
            pass
            
        if not ollama_ok:
            status = "FAIL"
            issues.append("Ollama daemon is offline. Inference requests will fail.")
        elif not model_ok:
            status = "WARNING"
            issues.append(f"Model '{settings.LLM_MODEL_NAME}' is not pulled in Ollama.")

        # 3. SQLite db check
        sqlite_ok = False
        try:
            import session_manager
            conn = session_manager.get_db_connection()
            conn.execute("SELECT 1").fetchone()
            conn.close()
            sqlite_ok = True
        except Exception:
            pass
            
        if not sqlite_ok:
            status = "FAIL"
            issues.append("SQLite database connection failed.")

        # 4. Memory/Disk thresholds
        disk = shutil.disk_usage("/")
        disk_free_gb = disk.free / (1024 ** 3)
        if disk_free_gb < 2.0:
            status = "WARNING"
            issues.append(f"Disk space is extremely low: {disk_free_gb:.1f} GB free.")

        mem = psutil.virtual_memory()
        ram_free_gb = mem.available / (1024 ** 3)
        if ram_free_gb < 0.5:
            status = "WARNING"
            issues.append(f"Available memory is extremely low: {ram_free_gb:.1f} GB free.")

        report = {
            "status": status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "checks": {
                "tesseract_ocr_installed": "PASS" if tesseract_ok else "WARNING",
                "ollama_responsive": "PASS" if ollama_ok else "FAIL",
                "target_model_pulled": "PASS" if model_ok else "WARNING",
                "sqlite_database_healthy": "PASS" if sqlite_ok else "FAIL",
                "disk_space_sufficient": "PASS" if disk_free_gb >= 2.0 else "WARNING",
                "ram_sufficient": "PASS" if ram_free_gb >= 0.5 else "WARNING"
            },
            "warnings_and_errors": issues
        }
        
        # Write report file
        try:
            with open("deployment_report.json", "w") as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save deployment report: {e}")
            
        return report

import time
deployment_validator = DeploymentValidator()
