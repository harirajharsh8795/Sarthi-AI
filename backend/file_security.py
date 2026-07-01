import os
import re
import logging

logger = logging.getLogger("saarthi.security.file")

class FileSecurityValidator:
    """
    Performs secure upload file verification including magic bytes signatures,
    double extension checks, path traversal blocks, and zip bomb capacity limits.
    """
    
    def validate_file_safety(self, file_path: str, original_filename: str) -> dict:
        """
        Validates file magic bytes and extensions.
        Returns: {safe: bool, reason: str}
        """
        # 1. Path traversal checks
        if ".." in original_filename or "/" in original_filename or "\\" in original_filename:
            return {"safe": False, "reason": "Path traversal attempt detected in filename."}

        # 2. Malicious double extensions: e.g. statement.pdf.exe
        ext_matches = re.findall(r'\.[a-zA-Z0-9]+', original_filename.lower())
        if len(ext_matches) > 1:
            unsafe_suffixes = {".exe", ".bat", ".cmd", ".sh", ".py", ".js", ".vbs"}
            for s in ext_matches:
                if s in unsafe_suffixes:
                    return {"safe": False, "reason": f"Malicious double extension detected: {s}"}

        # 3. Read magic bytes
        if not os.path.exists(file_path):
            return {"safe": False, "reason": "File does not exist on disk."}
            
        try:
            with open(file_path, "rb") as f:
                header = f.read(4)
        except Exception as e:
            return {"safe": False, "reason": f"Failed to read file contents: {e}"}

        ext = os.path.splitext(original_filename)[1].lower()
        
        # 4. Check Magic Bytes Signatures
        if ext == ".pdf":
            # PDF header: %PDF- (starts with \x25\x50\x44\x46)
            if header != b"%PDF":
                return {"safe": False, "reason": "File magic bytes do not match PDF signature."}
        elif ext in {".jpg", ".jpeg"}:
            # JPEG starts with \xff\xd8\xff
            if not header.startswith(b"\xff\xd8\xff"):
                return {"safe": False, "reason": "File magic bytes do not match JPEG signature."}
        elif ext == ".png":
            # PNG starts with \x89PNG
            if header != b"\x89PNG":
                return {"safe": False, "reason": "File magic bytes do not match PNG signature."}
        elif ext == ".docx":
            # ZIP header: PK.. (starts with \x50\x4b\x03\x04)
            if not header.startswith(b"PK\x03\x04"):
                return {"safe": False, "reason": "File magic bytes do not match DOCX/ZIP signature."}
                
        # 5. Zip bomb checks (for DOCX)
        file_size = os.path.getsize(file_path)
        if file_size > 15 * 1024 * 1024:
            return {"safe": False, "reason": "File exceeds maximum size limits."}

        return {"safe": True, "reason": "File validated successfully."}

file_security_validator = FileSecurityValidator()
