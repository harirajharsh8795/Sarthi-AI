import os
import psutil
import shutil
import requests
from config import settings

class SystemDiagnostics:
    """
    Analyzes system state to diagnose deployment issues,
    providing recommendations and overall health indicators.
    """
    
    def diagnose_system(self) -> dict:
        warnings = []
        recommendations = []
        overall_health = "Excellent"
        
        # 1. Check Tesseract OCR path
        tesseract_ok = bool(shutil.which("tesseract"))
        if not tesseract_ok:
            user_profile = os.environ.get("USERPROFILE", "")
            tess_path = os.path.join(user_profile, "AppData", "Local", "Tesseract-OCR", "tesseract.exe")
            if os.path.exists(tess_path):
                tesseract_ok = True
                
        if not tesseract_ok:
            overall_health = "Warning"
            warnings.append("OCR_TESSERACT_MISSING")
            recommendations.append(
                "Install Tesseract OCR (v5.0+) or add its installation folder to the Windows System PATH. "
                "Without it, image uploads will fail to parse."
            )

        # 2. Check Ollama responsiveness
        ollama_ok = False
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=1.0)
            if r.status_code == 200:
                ollama_ok = True
        except Exception:
            pass
            
        if not ollama_ok:
            overall_health = "Critical"
            warnings.append("OLLAMA_SERVICE_OFFLINE")
            recommendations.append(
                "Launch the Ollama desktop app or restart the Ollama service daemon. "
                "Ensure it is reachable on port 11434."
            )

        # 3. Check memory pressure
        mem = psutil.virtual_memory()
        free_ram_gb = mem.available / (1024 ** 3)
        if free_ram_gb < 1.0:
            if overall_health != "Critical":
                overall_health = "Warning"
            warnings.append("MEMORY_PRESSURE_HIGH")
            recommendations.append(
                f"Close heavy background applications. Free memory is currently {free_ram_gb:.2f} GB. "
                "NVIDIA Jetson devices should enable swap file configurations (e.g. 4GB swap space)."
            )

        # 4. Check disk capacity
        disk = shutil.disk_usage("/")
        free_disk_gb = disk.free / (1024 ** 3)
        if free_disk_gb < 3.0:
            if overall_health != "Critical":
                overall_health = "Warning"
            warnings.append("DISK_SPACE_LOW")
            recommendations.append(
                f"Free up disk space. Current capacity is {free_disk_gb:.1f} GB. "
                "ChromaDB and model storage require active disk writes."
            )

        # 5. Check SQLite DB locks
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
            overall_health = "Critical"
            warnings.append("DATABASE_UNREACHABLE")
            recommendations.append(
                "Check read/write permissions on './data/sqlite/saarthi.db'. "
                "If it is locked by another process, kill existing python tasks."
            )

        return {
            "overall_health": overall_health,
            "warnings": warnings,
            "recommended_actions": recommendations,
            "system_state": {
                "free_ram_gb": round(free_ram_gb, 2),
                "free_disk_gb": round(free_disk_gb, 2),
                "ollama_active": ollama_ok,
                "database_active": sqlite_ok
            }
        }

system_diagnostics = SystemDiagnostics()
