import os
import re
import json
import logging
from config import settings

logger = logging.getLogger("saarthi.security.scanner")

class SecretScanner:
    """
    Scans files and configuration files for hardcoded API keys,
    passwords, tokens, or credentials leaks.
    """
    
    def __init__(self):
        # Regex check indicators for common keys and secrets
        self.secret_regexes = {
            "api_key": r'(?i)(api_key|apikey|api-key)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,64}["\']',
            "password": r'(?i)(password|passwd|pwd)\s*[:=]\s*["\'][a-zA-Z0-9_\-\@\#\$]{6,32}["\']',
            "token": r'(?i)(token|jwt)\s*[:=]\s*["\'][a-zA-Z0-9_\-\.]{32,512}["\']',
            "private_key": r'-----BEGIN\s+PRIVATE\s+KEY-----'
        }

    def scan_project_secrets(self) -> dict:
        """
        Scans settings files and workspace directories for hardcoded credentials.
        Generates secret_scan_report.json.
        """
        leaks = []
        
        # Files to scan (target critical settings, configs and envs)
        scan_files = [".env", "config.py", "main.py", "db_manager.py"]
        
        for file_name in scan_files:
            file_path = os.path.join(os.getcwd(), file_name)
            if not os.path.exists(file_path):
                continue
                
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    
                for key_type, regex in self.secret_regexes.items():
                    matches = re.findall(regex, content)
                    if matches:
                        leaks.append({
                            "file": file_name,
                            "type_detected": key_type,
                            "match_count": len(matches)
                        })
            except Exception as e:
                logger.error(f"Failed to scan file {file_name}: {e}")

        status = "SECURE" if not leaks else "EXPOSED"
        report = {
            "status": status,
            "timestamp": time_str(),
            "scanned_files": scan_files,
            "detected_leaks": leaks,
            "total_leaks": len(leaks)
        }
        
        # Save report
        try:
            with open("secret_scan_report.json", "w") as f:
                json.dump(report, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save secret scan report: {e}")
            
        return report

def time_str():
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S")

secret_scanner = SecretScanner()
