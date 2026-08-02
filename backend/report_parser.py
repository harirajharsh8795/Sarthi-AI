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
    # Strategy 4: Numeric test result lines (e.g. "Serum SGPT (ALT) 78.32 10-40 IU/L" or "Serum Bilirubin Total 1.9")
    numeric_re = re.compile(r"^([A-Za-z0-9\s\(\)/-]{3,60}?)\s+([\d\.]+)\s*([A-Za-z%/µmglIU]+)?(?:\s+[\d\.-]+)?", re.IGNORECASE)
    for ln in lines:
        m = numeric_re.match(ln)
        if m:
            test = m.group(1).strip(' .:-\t')
            val = m.group(2).strip()
            unit = (m.group(3) or "").strip()
            res_str = f"{val} {unit}".strip()
            # Exclude header words or non-test strings
            if test.lower() not in ("test", "patient name", "reg no", "sample id", "bed no", "print time", "age", "sex", "method", "unit") and len(test) >= 3:
                if not any(t["test_name"] == test for t in results):
                    results.append({"test_name": test, "result": res_str, "raw": ln})

    return results


def extract_demographics_from_text(text: str) -> Dict[str, str]:
    """
    Extracts key patient demographics (Patient Name, Hospital/Lab, Ref Doctor, Age, Sex)
    from OCR'd text using robust multi-pattern regex matching.
    """
    if not text:
        return {}

    demographics = {}

    # 1. Patient Name Regexes
    name_patterns = [
        r"(?:Patient\s*Name|Pt\.?\s*Name|Patient|Name of Patient)\s*[:\-]\s*([A-Za-z\.\s]{3,45})",
        r"(?:Mrs\.|Mr\.|Ms\.|Master|Baby|Dr\.)\s+([A-Za-z\s]{3,40})",
        r"Name\s*[:\-]\s*([A-Za-z\.\s]{3,45})"
    ]
    for pat in name_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip(' .:-\t')
            if len(val) >= 3 and val.lower() not in ("not specified", "patient name", "unknown", "test", "name"):
                demographics["patient_name"] = val
                break

    # 2. Hospital / Lab Name Regexes
    hosp_patterns = [
        r"(?:Hospital|Lab|Diagnostic|Pathology|Clinic|Center|Centre|Laboratory)\s*[:\-]\s*([A-Za-z0-9\.\s&]{3,50})",
        r"([A-Za-z\s&]{3,40}(?:Hospital|Diagnostic|Pathology|Lab|Clinic|Center))"
    ]
    for pat in hosp_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip(' .:-\t')
            if len(val) >= 4 and val.lower() not in ("hospital", "laboratory", "lab"):
                demographics["hospital_name"] = val
                break

    # 3. Doctor Name Regexes
    doc_patterns = [
        r"(?:Ref\.?\s*By|Ref\.?\s*Doctor|Doctor|Dr\.?\s*Name|Referring Doctor)\s*[:\-]\s*([A-Za-z\.\s]{3,40})"
    ]
    for pat in doc_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip(' .:-\t')
            if len(val) >= 3:
                demographics["ref_doctor"] = val
                break

    # 4. Age / Sex Regexes
    age_patterns = [
        r"(?:Age\s*/\s*(?:Sex|Gender)|Age|Gender|Sex)\s*[:\-]\s*([\d\sA-Za-z/,\.-]{2,25})"
    ]
    for pat in age_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            val = m.group(1).strip(' .:-\t')
            if len(val) >= 2:
                demographics["age_sex"] = val
                break

    return demographics
