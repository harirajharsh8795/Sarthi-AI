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
        urls_to_try = [settings.OLLAMA_URL]
        if "localhost" in settings.OLLAMA_URL:
            urls_to_try.append(settings.OLLAMA_URL.replace("localhost", "127.0.0.1"))
        if "localhost" in settings.OLLAMA_URL or "127.0.0.1" in settings.OLLAMA_URL:
            urls_to_try.append(settings.OLLAMA_URL.replace("localhost", "172.17.0.1").replace("127.0.0.1", "172.17.0.1"))

        for url in urls_to_try:
            try:
                base_url = url.replace("/api/generate", "")
                r = requests.get(f"{base_url}/api/tags", timeout=1.0)
                if r.status_code == 200:
                    ollama_ok = True
                    if url != settings.OLLAMA_URL:
                        settings.OLLAMA_URL = url
                    models = [m["name"] for m in r.json().get("models", [])]
                    if any(settings.LLM_MODEL_NAME in m or m in settings.LLM_MODEL_NAME for m in models):
                        model_ok = True
                    break
            except Exception:
                continue

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

        # 4. Voice dependencies check
        voice_ok = True
        try:
            import whisper
            import pyttsx3
            engine = pyttsx3.init()
            del engine
        except Exception as e:
            voice_ok = False
            status = "WARNING"
            issues.append(f"Voice pipeline dependencies check failed: {e}")

        # 5. FFmpeg binary check
        ffmpeg_ok = False
        if shutil.which("ffmpeg"):
            ffmpeg_ok = True
        else:
            user_profile = os.environ.get("USERPROFILE", "")
            winget_link = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Links", "ffmpeg.exe")
            if os.path.exists(winget_link):
                ffmpeg_ok = True
            else:
                packages_dir = os.path.join(user_profile, "AppData", "Local", "Microsoft", "WinGet", "Packages")
                if os.path.exists(packages_dir):
                    for root, dirs, files in os.walk(packages_dir):
                        if "ffmpeg.exe" in files:
                            ffmpeg_ok = True
                            break
        if not ffmpeg_ok:
            status = "WARNING"
            issues.append("FFmpeg executable not found. Whisper transcription will fail.")

        # 6. Memory/Disk thresholds
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
                "voice_dependencies_healthy": "PASS" if voice_ok else "WARNING",
                "ffmpeg_installed": "PASS" if ffmpeg_ok else "WARNING",
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
