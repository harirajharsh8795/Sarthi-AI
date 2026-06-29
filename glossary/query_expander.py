import os
import json
import re
import difflib

# Resolve the glossary path relative to this file
GLOSSARY_PATH = os.path.join(os.path.dirname(__file__), "hinglish_medical_terms.json")

def load_glossary():
    try:
        with open(GLOSSARY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load medical glossary from {GLOSSARY_PATH}: {e}")
        return {}

# Load the glossary once at module load
GLOSSARY = load_glossary()

def expand_query_with_glossary(query: str) -> str:
    """
    Expands Hindi/Hinglish colloquial medical terms in a query with their 
    standard clinical English equivalents based on a local glossary.
    
    Supports both Romanized Hinglish (using exact regex and fuzzy edit-distance matching)
    and Devanagari script (using substring checks) to avoid false positive matches.
    """
    if not query or not GLOSSARY:
        return query

    # Find matches
    matched_clinical_terms = []
    
    # We will search the query case-insensitively
    query_lower = query.lower()
    query_words = re.findall(r"\w+", query_lower)
    
    for key, clinical_terms in GLOSSARY.items():
        key_lower = key.lower()
        
        # Check if the key contains Devanagari characters
        is_devanagari = any(ord(char) >= 0x0900 and ord(char) <= 0x097F for char in key_lower)
        
        matched = False
        if is_devanagari:
            if key_lower in query_lower:
                matched = True
        else:
            # 1. Try exact word boundary match
            pattern = r"\b" + re.escape(key_lower) + r"\b"
            if re.search(pattern, query_lower):
                matched = True
            else:
                # 2. Try fuzzy close matching with edit distance (cutoff=0.8)
                key_words = key_lower.split()
                if key_words and query_words:
                    if len(key_words) == 1:
                        # Check if key matches any query word close enough
                        close_matches = difflib.get_close_matches(key_words[0], query_words, n=1, cutoff=0.8)
                        if close_matches:
                            matched = True
                    else:
                        # Multi-word key: check for contiguous matching words
                        nk = len(key_words)
                        nq = len(query_words)
                        for i in range(nq - nk + 1):
                            sub_slice = query_words[i:i+nk]
                            match_count = 0
                            for kw, qw in zip(key_words, sub_slice):
                                if difflib.get_close_matches(kw, [qw], n=1, cutoff=0.8):
                                    match_count += 1
                                else:
                                    break
                            if match_count == nk:
                                matched = True
                                break
                                
        if matched:
            for term in clinical_terms:
                if term not in matched_clinical_terms:
                    matched_clinical_terms.append(term)
                    
    if matched_clinical_terms:
        # Append clinical terms in parentheses for search expansion
        expansion_suffix = f" ({', '.join(matched_clinical_terms)})"
        return query + expansion_suffix
        
    return query

# Future scope note: This glossary is a deterministic starting point.
# It can be expanded or updated over time based on user feedback and retrieval logs,
# which keeps the system explainable and avoids high resource/GPU fine-tuning needs.
