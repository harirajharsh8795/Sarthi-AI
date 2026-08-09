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

    # Strategy 0: Explicit Serology / Rapid Spot Tests (HBS AG SPOT, HIV SPOT, HCV SPOT, DENGUE, VDRL, etc.)
    serology_re = re.compile(
        r"(HBS\s*AG(?:\s*SPOT)?|HIV(?:\s*SPOT)?|HCV(?:\s*SPOT)?|ANTI\s*HCV|DENGUE\s*NS1|TYPHIDOT|VDRL|SYPHILIS|COVID\s*RAPID)\b[\s\S]*?(NON\s*-?\s*REACTIVE|REACTIVE|POSITIVE|NEGATIVE|NOT\s+DETECTED|DETECTED)",
        re.IGNORECASE
    )
    for m in serology_re.finditer(text):
        t_name = m.group(1).strip().upper()
        raw_res = m.group(2).strip()
        norm_res = _normalize_result(raw_res)
        if not any(r["test_name"] == t_name for r in results):
            results.append({"test_name": t_name, "result": norm_res, "raw": f"{t_name} -> {norm_res}"})

    # Strategy 1: lines that end with a known token, e.g. "HCV SPOT    NON REACTIVE"
    token_re = re.compile(r"(.{3,80}?)\s{2,}\s*(NON\s*-?\s*REACTIVE|REACTIVE|POSITIVE|NEGATIVE|NOT\s+DETECTED|DETECTED)\b", re.IGNORECASE)
    for ln in lines:
        m = token_re.search(ln)
        if m:
            test = m.group(1).strip(' .:-\t')
            raw_res = m.group(2).strip()
            if not any(r["test_name"] == test for r in results):
                results.append({"test_name": test, "result": _normalize_result(raw_res), "raw": raw_res})

    # Strategy 2: lines that look like "Test Name : Result" or "Test Name : 12.3 U/L"
    colon_re = re.compile(r"^(.{3,80}?)\s*:\s*(.+)$")
    for ln in lines:
        m = colon_re.match(ln)
        if m:
            test = m.group(1).strip(' .:-\t')
            raw_res = m.group(2).strip()
            if not any(t["test_name"] == test for t in results):
                normalized = None
                for tok in COMMON_RESULT_TOKENS:
                    if tok in raw_res.upper():
                        normalized = _normalize_result(tok)
                        break
                results.append({"test_name": test, "result": normalized or raw_res, "raw": raw_res})

    # Strategy 4: Numeric test result lines (e.g. "Serum SGPT (ALT) 78.32 10-40 IU/L" or "Serum Bilirubin Total 1.9")
    numeric_re = re.compile(r"^([A-Za-z0-9\s\(\)/-]{3,60}?)\s+([\d\.]+)\s*([A-Za-z%/µmglIU]+)?(?:\s+[\d\.-]+)?", re.IGNORECASE)
    for ln in lines:
        m = numeric_re.match(ln)
        if m:
            test = m.group(1).strip(' .:-\t')
            val = m.group(2).strip()
            unit = (m.group(3) or "").strip()
            res_str = f"{val} {unit}".strip()
            if test.lower() not in ("test", "patient name", "reg no", "sample id", "bed no", "print time", "age", "sex", "method", "unit") and len(test) >= 3:
                if not any(t["test_name"] == test for t in results):
                    results.append({"test_name": test, "result": res_str, "raw": ln})

    return results


def extract_demographics_from_text(text: str) -> Dict[str, str]:
    """
    Extracts key patient demographics (Patient Name, Hospital/Lab, Ref Doctor, Age, Sex)
    from OCR'd text using robust line-by-line regex matching.
    """
    if not text:
        return {}

    demographics = {}
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # 1. Patient Name Regexes
    name_patterns = [
        r"(?:Patient\s*Name|Pt\.?\s*Name|Patient|Name of Patient|Patient's\s*Name)\s*[:\-]?\s*([A-Za-z\.\s]{2,40})",
        r"(?:Mrs\.|Mr\.|Ms\.|Master|Baby|Dr\.|Smt\.|Shri|Sh\.)\s+([A-Za-z\s]{2,35})",
        r"\bName\s*[:\-]\s*([A-Za-z\.\s]{2,40})"
    ]
    for ln in lines:
        for pat in name_patterns:
            m = re.search(pat, ln, re.IGNORECASE)
            if m:
                val = m.group(0).strip(' .:-\t\r\n')
                if "name" in val.lower() and ":" in val:
                    val = val.split(":", 1)[1].strip()
                elif "name" in val.lower() and "-" in val:
                    val = val.split("-", 1)[1].strip()
                val = re.sub(r"\s+(?:Bill|MR|Reg|Age|Sex|Date|Ward|No|ID|Sample|Type|Reported|Collected).*", "", val, flags=re.IGNORECASE).strip()
                if len(val) >= 3 and val.lower() not in ("not specified", "patient name", "unknown", "test", "name", "report", "gender", "age"):
                    demographics["patient_name"] = val
                    break
        if "patient_name" in demographics:
            break

    # 2. Hospital / Lab Name Regexes
    hosp_patterns = [
        r"(HOLY\s*FAMILY\s*HOSPITAL)",
        r"(INAMDAR\s*MULTISPECIALITY\s*HOSPITAL)",
        r"([A-Za-z0-9\s&]{3,45}(?:Hospital|Diagnostic|Pathology|Lab|Clinic|Center|Centre|Laboratory))",
        r"(?:Hospital|Lab|Diagnostic|Pathology|Clinic|Center|Centre|Laboratory)\s*[:\-]?\s*([A-Za-z0-9\.\s&]{3,45})"
    ]
    for ln in lines[:10]: # Check top 10 lines of document
        for pat in hosp_patterns:
            m = re.search(pat, ln, re.IGNORECASE)
            if m:
                val = m.group(1).strip(' .:-\t\r\n')
                if len(val) >= 4 and val.lower() not in ("hospital", "laboratory", "lab", "pathology", "clinic"):
                    demographics["hospital_name"] = val
                    break
        if "hospital_name" in demographics:
            break

    # 3. Doctor Name Regexes
    doc_patterns = [
        r"(?:Admitting\s*Doc\.?|Ref\.?\s*By|Ref\.?\s*Doctor|Doctor|Dr\.?\s*Name|Referring Doctor|Consultant)\s*[:\-]?\s*([A-Za-z\.\s]{3,35})",
        r"(Dr\.\s*[A-Za-z\s]{3,30})"
    ]
    for ln in lines:
        for pat in doc_patterns:
            m = re.search(pat, ln, re.IGNORECASE)
            if m:
                val = m.group(1).strip(' .:-\t\r\n')
                val = re.sub(r"\s+(?:Approved|Reported|Collected|Bill|Ward|MD|Pathologist|MBBS|Reg|Sample|ID|Date|Time).*", "", val, flags=re.IGNORECASE).strip()
                if len(val) >= 4 and val.lower() not in ("doctor", "ref doctor", "admitting doc"):
                    demographics["ref_doctor"] = val
                    break
        if "ref_doctor" in demographics:
            break

    # 4. Age / Sex Regexes
    for ln in lines:
        m = re.search(r"(?:Age\s*/\s*(?:Sex|Gender)|Age|Gender|Sex)\s*[:\-]?\s*([^\n\r]{2,40})", ln, re.IGNORECASE)
        if m:
            val = m.group(1).strip(' .:-\t\r\n')
            val = re.sub(r"\s+(?:Reported|Approved|Collected|Ref|Doctor|Ward|Bill|Date|Time).*", "", val, flags=re.IGNORECASE).strip()
            if len(val) >= 2:
                demographics["age_sex"] = val
                break

    return demographics


def infer_organ_system_from_text(text: str) -> str:
    """
    Infers organ system / test category from text to prevent disease hallucinations.
    """
    if not text:
        return ""

    t_upper = text.upper()

    # Serology / Viral Markers (HIV, HBsAg, HCV)
    if any(k in t_upper for k in ["HIV", "HBSAG", "HCV", "SEROLOGY", "VDRL", "DENGUE"]):
        return "Lab Serology / Viral Markers Screening (HBsAg, HIV 1&2, Anti-HCV)"
    # Liver Function Test (LFT)
    if any(k in t_upper for k in ["BILIRUBIN", "SGPT", "SGOT", "ALT", "AST", "LIVER", "ALKALINE PHOSPHATASE"]):
        return "Liver Function Test (LFT) / Hepatic Parameters"
    # Kidney Function Test (KFT)
    if any(k in t_upper for k in ["CREATININE", "UREA", "URIC ACID", "KIDNEY", "RENAL"]):
        return "Kidney Function Test (KFT) / Renal Parameters"
    # Complete Blood Count (CBC)
    if any(k in t_upper for k in ["HEMOGLOBIN", "PLATELET", "WBC", "RBC", "TLC", "DLC", "NEUTROPHIL", "LYMPHOCYTE"]):
        return "Complete Blood Count (CBC) / Hematology Report"
    # Lipid Profile
    if any(k in t_upper for k in ["CHOLESTEROL", "TRIGLYCERIDES", "HDL", "LDL", "LIPID"]):
        return "Lipid Profile / Cardiovascular Test"
    # Diabetes / Glucose
    if any(k in t_upper for k in ["GLUCOSE", "HBA1C", "FASTING BLOOD SUGAR", "PPBS", "INSULIN"]):
        return "Blood Sugar / Diabetes Report"

    return ""
