import re
from typing import List, Dict

"""
Simple deterministic parser for common lab report lines.
Extracts test name → result pairs from OCR'd text to avoid LLM hallucinations.
"""

COMMON_RESULT_TOKENS = [
    "NON REACTIVE",
    "NON-REACTIVE",
    "REACTIVE",
    "POSITIVE",
    "NEGATIVE",
    "NOT DETECTED",
    "DETECTED",
    "NON REACTIVE (Negative)",
]


def _normalize_result(raw: str) -> str:
    if not raw:
        return raw
    r = raw.strip().upper()
    r = re.sub(r"\s+-\s+", " ", r)
    # normalize common variants
    if "NON" in r and "REACT" in r:
        return "NON REACTIVE (Negative)"
    if r in ("NOT DETECTED", "NEGATIVE"):
        return "NON REACTIVE (Negative)"
    if r == "DETECTED" or r == "REACTIVE" or r == "POSITIVE":
        return r
    # numeric or united results: keep as-is (trim)
    return raw.strip()


def extract_test_results_from_text(text: str) -> List[Dict[str, str]]:
    """
    Returns a list of dicts: [{"test_name": .., "result": .., "raw": ..}, ...]

    The function uses multiple regex strategies to handle typical lab report formats.
    """
    if not text:
        return []

    lines = [l.strip() for l in text.splitlines() if l.strip()]
    results = []

    # Strategy 1: lines that end with a known token, e.g. "HCV SPOT    NON REACTIVE"
    token_re = re.compile(r"(.{3,80}?)\s{2,}\s*(NON\s*-?\s*REACTIVE|REACTIVE|POSITIVE|NEGATIVE|NOT\s+DETECTED|DETECTED)\b", re.IGNORECASE)
    for ln in lines:
        m = token_re.search(ln)
        if m:
            test = m.group(1).strip(' .:-\t')
            raw_res = m.group(2).strip()
            results.append({"test_name": test, "result": _normalize_result(raw_res), "raw": raw_res})

    # Strategy 2: lines that look like "Test Name : Result" or "Test Name : 12.3 U/L"
    colon_re = re.compile(r"^(.{3,80}?)\s*:\s*(.+)$")
    for ln in lines:
        m = colon_re.match(ln)
        if m:
            test = m.group(1).strip(' .:-\t')
            raw_res = m.group(2).strip()
            # Avoid double-adding if already captured
            if any(t["test_name"] == test for t in results):
                continue
            # If raw_res includes known tokens, normalize; else include as-is
            normalized = None
            for tok in COMMON_RESULT_TOKENS:
                if tok in raw_res.upper():
                    normalized = _normalize_result(tok)
                    break
            results.append({"test_name": test, "result": normalized or raw_res, "raw": raw_res})

    # Strategy 3: Inline patterns like "HBS AG SPOT\nNON REACTIVE" — look at pairs of consecutive lines
    for i in range(len(lines) - 1):
        a = lines[i]
        b = lines[i + 1]
        if any(tok in b.upper() for tok in COMMON_RESULT_TOKENS):
            test = a.strip(' .:-\t')
            raw_res = b.strip()
            if test and not any(t["test_name"] == test for t in results):
                results.append({"test_name": test, "result": _normalize_result(raw_res), "raw": raw_res})

    return results
