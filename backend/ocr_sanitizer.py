import re
import unicodedata
import logging

logger = logging.getLogger("saarthi.security.ocr")

class OCRSanitizer:
    """
    Cleans OCR output before entering RAG embedding chunking.
    Strips hidden unicode BOMs, control characters, and normalizes encodings.
    Performs OCR quality assessment and conservative post-OCR text repair.
    """
    
    def sanitize_ocr_text(self, text: str) -> str:
        """Normalizes encodings, purges hidden characters, and performs conservative post-OCR text repair."""
        if not text:
            return ""

        # 1. Normalize unicode characters (NFKC normalization)
        normalized = unicodedata.normalize('NFKC', text)
        
        # 2. Remove byte order marks (BOM) & zero-width characters
        normalized = normalized.replace('\ufeff', '').replace('\u200b', '')
        
        # 3. Strip control characters (ascii 0-31 except newlines and tabs)
        sanitized = "".join(ch for ch in normalized if ord(ch) >= 32 or ch in ['\n', '\t'])
        
        # 4. Remove excessive whitespaces/newlines
        sanitized = re.sub(r'[ \t]+', ' ', sanitized)
        sanitized = re.sub(r'\n{3,}', '\n\n', sanitized)

        # 5. Perform conservative post-OCR text repair
        repaired = self.repair_ocr_text(sanitized.strip())

        return repaired

    def repair_ocr_text(self, text: str) -> str:
        """
        Applies conservative post-OCR text repairs:
        1. Collapse excessive spaces between single letters of the same word (e.g. 'S A N T O S H' -> 'SANTOSH').
        2. Insert spaces between merged camelCase words (e.g. 'nonReactive' -> 'non Reactive').
        
        CONSERVATIVE SAFETY GUARANTEE:
        - Does NOT over-correct legitimate uppercase acronyms or medical/legal codes (e.g. 'HBsAg', 'IPC-302', 'ICD-10').
        - Preserves single-character English words ('a', 'I', 'A') and Devanagari numerals.
        """
        if not text:
            return ""

        repaired = text

        # Repair 1: Spaced-out letters in individual words
        # Matches 3 or more single capital/lowercase letters separated by single spaces (e.g. "S A N T O S H")
        def _collapse_spaced_letters(match):
            raw = match.group(0)
            collapsed = re.sub(r'\s+', '', raw)
            return collapsed

        # Spaced-out uppercase sequence (e.g. "S A N T O S H  D E V I" -> "SANTOSH DEVI")
        repaired = re.sub(r'\b(?:[A-Z]\s+){2,}[A-Z]\b', _collapse_spaced_letters, repaired)

        # Repair 2: Merged lowercase-Capital words (e.g. "nonReactive" -> "non Reactive", "hepatitisC" -> "hepatitis C")
        def _fix_camelcase_merge(match):
            prefix = match.group(1)
            suffix = match.group(2)
            if prefix.lower() in ["hb", "mr", "qp"] or prefix in ["HBs", "m", "qp"]:
                return match.group(0)
            return f"{prefix} {suffix}"

        repaired = re.sub(r'([a-z]{2,})([A-Z][a-z]+)', _fix_camelcase_merge, repaired)

        return repaired

    def assess_ocr_quality(self, text: str) -> dict:
        """
        Assesses OCR quality score (0.0 to 1.0) and flags common OCR degradation:
        - Ratio of isolated single-character tokens (broken spacing).
        - Ratio of garbled tokens containing mixed digits and special symbols inside words.
        - Ratio of non-readable noise characters.
        """
        if not text or not text.strip():
            return {
                "quality_score": 0.0,
                "is_low_quality": True,
                "single_char_word_ratio": 0.0,
                "garbled_token_ratio": 0.0,
                "noise_ratio": 0.0,
                "warnings": ["Empty or whitespace-only text"]
            }

        tokens = text.split()
        total_tokens = len(tokens)
        total_chars = len(text)

        # 1. Single character token ratio (excluding valid 1-char tokens 'a', 'i', 'I', 'A', numbers)
        single_chars = [t for t in tokens if len(t) == 1 and not t.isdigit() and t.lower() not in ['a', 'i']]
        single_char_ratio = len(single_chars) / total_tokens if total_tokens > 0 else 0.0

        # 2. Garbled token ratio (mixed digits & special chars inside alpha tokens e.g. H3p@t!t!$)
        garbled_tokens = [t for t in tokens if re.search(r'[A-Za-z]+[0-9@#$%^&*!~]+[A-Za-z]+', t)]
        garbled_ratio = len(garbled_tokens) / total_tokens if total_tokens > 0 else 0.0

        # 3. Noise character ratio (non-alphanumeric, non-whitespace, non-standard punctuation)
        noise_chars = re.findall(r'[^\w\s\.,\?!:;()\-\/\'\"]', text)
        noise_ratio = len(noise_chars) / total_chars if total_chars > 0 else 0.0

        # Calculate weighted quality score (1.0 = perfect quality, 0.0 = completely garbled)
        quality_score = 1.0 - (0.45 * single_char_ratio + 0.40 * garbled_ratio + 0.15 * noise_ratio)
        quality_score = min(max(round(quality_score, 2), 0.0), 1.0)

        is_low_quality = quality_score < 0.40
        warnings = []
        if single_char_ratio > 0.20:
            warnings.append(f"High single-character token ratio ({single_char_ratio:.2%}) — likely broken spacing")
        if garbled_ratio > 0.10:
            warnings.append(f"Garbled token ratio ({garbled_ratio:.2%}) — misread OCR symbols detected")
        if noise_ratio > 0.15:
            warnings.append(f"High noise character ratio ({noise_ratio:.2%})")

        return {
            "quality_score": quality_score,
            "is_low_quality": is_low_quality,
            "single_char_word_ratio": round(single_char_ratio, 2),
            "garbled_token_ratio": round(garbled_ratio, 2),
            "noise_ratio": round(noise_ratio, 2),
            "warnings": warnings
        }

    def detect_suspicious_patterns(self, text: str) -> bool:
        """Detects if text contains binary blocks, excessive non-ascii, or raw scripts."""
        if not text:
            return False
            
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

