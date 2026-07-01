import os
import zipfile
import time
import logging
import shutil

logger = logging.getLogger("saarthi.security.backup")

class BackupService:
    """
    Handles zipping, storing, and validating SQLite database backups,
    knowledge base metadata, and configuration files.
    """
    
    def __init__(self):
        self.backup_dir = "./data/backups"
        self.sqlite_db_path = "./data/sqlite/saarthi.db"

    def trigger_backup(self) -> dict:
        """
        Zips config and SQLite database to a dated backup file.
        """
        os.makedirs(self.backup_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_filename = f"saarthi_backup_{timestamp}.zip"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # 1. Backup SQLite database if exists
                if os.path.exists(self.sqlite_db_path):
                    zipf.write(self.sqlite_db_path, arcname="saarthi.db")
                # 2. Backup config
                if os.path.exists("config.py"):
                    zipf.write("config.py", arcname="config.py")
                    
            size_kb = os.path.getsize(backup_path) / 1024.0
            
            # Verify integrity
            integrity_ok = self.verify_backup_integrity(backup_path)
            
            return {
                "success": True,
                "backup_file": backup_filename,
                "size_kb": round(size_kb, 2),
                "integrity_check": "PASS" if integrity_ok else "FAIL"
            }
        except Exception as e:
            logger.error(f"Backup generation failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "integrity_check": "FAIL"
            }

    def verify_backup_integrity(self, zip_path: str) -> bool:
        """Tests zip file integrity using built-in ZIP testzip checks."""
        if not os.path.exists(zip_path):
            return False
            
        try:
            with zipfile.ZipFile(zip_path, 'r') as zipf:
                bad_file = zipf.testzip()
                if bad_file is not None:
                    logger.error(f"Corrupted file inside backup zip: {bad_file}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Backup validation failed: {e}")
            return False

backup_service = BackupService()
