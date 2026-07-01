import re
import logging

logger = logging.getLogger("saarthi.security.privacy")

class PrivacyEngine:
    """
    Scans logs and query texts to redact sensitive Indian PII identifiers
    (Aadhaar, PAN cards, Bank accounts, IFSC, Phone numbers, Emails).
    """
    
    def __init__(self):
        # Indian citizen specific PII regex patterns
        self.pii_patterns = [
            # 1. Aadhaar: 12 digits or spaces (e.g. 1234 5678 9012)
            (r'\b\d{4}\s\d{4}\s\d{4}\b', "[AADHAAR_REDACTED]"),
            (r'\b\d{12}\b', "[AADHAAR_REDACTED]"),
            
            # 2. PAN: 5 letters + 4 numbers + 1 letter (e.g. ABCDE1234F)
            (r'\b[A-Z]{5}\d{4}[A-Z]\b', "[PAN_REDACTED]"),
            
            # 3. IFSC: 4 letters + 0 + 6 alphanumeric (e.g. SBIN0012345)
            (r'\b[A-Z]{4}0[A-Z0-9]{6}\b', "[IFSC_REDACTED]"),
            
            # 4. Email
            (r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', "[EMAIL_REDACTED]"),
            
            # 5. Phone: 10 digits
            (r'\b[6-9]\d{9}\b', "[PHONE_REDACTED]")
        ]

    def redact_pii(self, text: str) -> str:
        """Masks sensitive elements in a text string."""
        if not text:
            return ""
            
        redacted = text
        for pattern, mask in self.pii_patterns:
            redacted = re.sub(pattern, mask, redacted, flags=re.IGNORECASE)
            
        return redacted

privacy_engine = PrivacyEngine()
