import re
import json
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.intent")

class IntentService:
    """
    Classifies language, domain, and user intent of incoming queries.
    Uses regex rules for fast paths, falling back to local llama3.2:1b for complex cases.
    """
    
    def detect_language(self, text: str) -> str:
        """Heuristic language detection (English vs Hindi vs Hinglish)."""
        if not text:
            return "English"
        
        # Devanagari range check
        if re.search(r'[\u0900-\u097f]', text):
            return "Hindi"
            
        # Common Hindi words written in English alphabet (Hinglish check)
        hinglish_markers = {
            "kya", "hai", "kaise", "batao", "mera", "jo", "karne", "karo", "kam", 
            "dawa", "ilaj", "bukhar", "khata", "paisa", "loan", "samjhao", "likho"
        }
        words = set(re.findall(r'\b\w+\b', text.lower()))
        if words.intersection(hinglish_markers):
            return "Hinglish"
            
        return "English"

    def detect_domain_and_intent_fast(self, text: str) -> tuple:
        """Regex-based classification for fast response paths."""
        text_lower = text.lower()
        
        # Greeting checks
        greetings = {"hello", "hi", "hey", "namaste", "pranam", "good morning", "good afternoon"}
        if text_lower.strip() in greetings:
            return "General", "Greeting", 1.0

        # Medical triggers
        medical_keywords = {
            "fever", "bukhar", "bhukhar", "pain", "dard", "doctor", "hospital", "illness", 
            "dawa", "dawai", "medicine", "symptoms", "treatment", "ilaj", "canc", "tb", "cough"
        }
        
        # Legal triggers
        legal_keywords = {
            "law", "court", "ipc", "crpc", "bnss", "fir", "police", "rti", "complaint", 
            "consumer", "advocate", "vakeel", "dhara", "kanoon", "rights"
        }
        
        # Banking triggers
        banking_keywords = {
            "bank", "kyc", "account", "rbi", "loan", "interest", "credit", "card", 
            "savings", "khata", "paisa", "atm", "transaction"
        }

        words = set(re.findall(r'\b\w+\b', text_lower))
        
        has_med = bool(words.intersection(medical_keywords))
        has_leg = bool(words.intersection(legal_keywords))
        has_bank = bool(words.intersection(banking_keywords))
        
        if has_med and not (has_leg or has_bank):
            return "Medical", "QA", 0.9
        if has_leg and not (has_med or has_bank):
            return "Legal", "QA", 0.9
        if has_bank and not (has_med or has_leg):
            return "Banking", "QA", 0.9
            
        return None, None, None

    def classify_query(self, text: str) -> dict:
        """
        Runs complete intent classification.
        Returns: {language, domain, intent, confidence_score, query_type}
        """
        lang = self.detect_language(text)
        
        # Try fast path
        domain, intent, conf = self.detect_domain_and_intent_fast(text)
        if domain and intent:
            return {
                "language": lang,
                "domain": domain,
                "intent": intent,
                "confidence_score": conf,
                "query_type": "Domain_QA" if intent == "QA" else "Conversation"
            }
            
        # Fallback to lightweight local LLM structural check
        # We instruct Ollama to output simple structural JSON format
        prompt = (
            f"Classify this user query:\n\"{text}\"\n\n"
            f"Output JSON with exact keys: \"domain\" (Medical, Legal, Banking, General), "
            f"\"intent\" (Greeting, Continuation, Ambiguous, Off_topic, QA), "
            f"\"query_type\" (Domain_QA, Conversation, Unknown).\n"
            f"Do not output explanation or conversation wrapper, only the JSON block."
        )
        
        try:
            r = requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": settings.LLM_MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.0}
                },
                timeout=5
            )
            if r.status_code == 200:
                resp = r.json().get("response", "").strip()
                # Find JSON block
                json_match = re.search(r'\{.*\}', resp, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    return {
                        "language": lang,
                        "domain": data.get("domain", "General"),
                        "intent": data.get("intent", "QA"),
                        "confidence_score": 0.85,
                        "query_type": data.get("query_type", "Domain_QA")
                    }
        except Exception as e:
            logger.warning(f"LLM classification fallback failed: {e}")
            
        # Hard fallback
        return {
            "language": lang,
            "domain": "General",
            "intent": "QA",
            "confidence_score": 0.5,
            "query_type": "Unknown"
        }

intent_service = IntentService()
