import re
import unicodedata
import logging

logger = logging.getLogger("saarthi.security.ocr")

class OCRSanitizer:
    """
    Cleans OCR output before entering RAG embedding chunking.
    Strips hidden unicode BOMs, control characters, and normalizes encodings.
    """
    
    def sanitize_ocr_text(self, text: str) -> str:
        """Normalizes and purges hidden characters or attacks from text."""
        if not text:
            return ""

        # 1. Normalize unicode characters (NFKC normalization)
        normalized = unicodedata.normalize('NFKC', text)
        
        # 2. Remove byte order marks (BOM) & zero-width characters
        normalized = normalized.replace('\ufeff', '').replace('\u200b', '')
        
        # 3. Strip control characters (ascii 0-31 except newlines and tabs)
        # keeping \n (10) and \t (9)
        sanitized = "".join(ch for ch in normalized if ord(ch) >= 32 or ch in ['\n', '\t'])
        
        # 4. Remove excessive whitespaces/newlines
        sanitized = re.sub(r'[ \t]+', ' ', sanitized)
        sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)

        return sanitized.strip()

    def detect_suspicious_patterns(self, text: str) -> bool:
        """Detects if text contains binary blocks, excessive non-ascii, or raw scripts."""
        if not text:
            return False
            
        # If the ratio of non-readable character sets is high, flag it
        total_len = len(text)
        if total_len == 0:
            return False
            
        non_readable = len(re.findall(r'[^\w\s\.,\?!-]', text))
        ratio = non_readable / total_len
        if ratio > 0.40:
            logger.warning(f"Suspicious character ratio detected in OCR output: {ratio:.2f}")
            return True
            
        # Check for inline script tag injections
        if re.search(r'<script.*?>', text, re.IGNORECASE):
            return True
            
        return False

ocr_sanitizer = OCRSanitizer()
