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
            # Questions
            "kya", "kaise", "kyun", "kab", "kahan", "kaun", "kisko", "kitna", "kidhar", "kaunsa",
            # Pronouns/Subjects
            "main", "mera", "meri", "mere", "hum", "hamara", "tum", "tumhara", "tu", "tera",
            "aap", "aapka", "woh", "wo", "yeh", "ye", "uska", "unki", "unka", "mujhe", "hamein", "tumhe", "aapko",
            # Verbs (Base & Conjugations)
            "hai", "hain", "h", "tha", "thi", "hoga", "hogi", "hoge",
            "karo", "kro", "kare", "karna", "karne", "kar", "kiya", "kijiye",
            "batao", "btao", "batai", "batana", "samjhao", "smjhao", "samajh", "likho", "likhna",
            "dekh", "dekho", "dekha", "sun", "suno", "suna", "bol", "bolo", "bola",
            "jao", "jana", "gaya", "aao", "aana", "aaya", "khao", "khana",
            "chahiye", "chahye", "mila", "milega", "sakte", "sakti", "sakta",
            "raha", "rha", "rahe", "rhe", "rahi", "rhi",
            # Conjunctions/Prepositions
            "aur", "ya", "par", "lekin", "magar", "kyunki", "isliye", "agar",
            "ka", "ke", "ki", "ko", "se", "mein", "me", "tak", "liye", "saath",
            # Common Nouns
            "kam", "kaam", "naam", "baat", "din", "raat", "aaj", "kal", "samay",
            "paisa", "paise", "rupay", "khata", "byaj",
            "dawa", "dawai", "ilaj", "bukhar", "dard", "bimari",
            "kanoon", "niyam", "adhikar", "shikayat", "faisla"
        }
        words = set(re.findall(r'\b[a-zA-Z]+\b', text.lower()))
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

        # Medical triggers (includes common Hinglish misspellings)
        medical_keywords = {
            "fever", "bukhar", "bhukhar", "bhukar", "bukhr", "bukhaar",
            "pain", "dard", "drd",
            "doctor", "hospital", "illness", "bimari", "bimaari", "beemar", "bimar",
            "dawa", "dawai", "dvai", "dvaii", "dawaii", "medicine", "goli",
            "symptoms", "treatment", "ilaj", "ilaaj",
            "canc", "cancer", "tb", "cough", "khansi", "khaansi",
            "sehat", "health", "patient", "mareez",
            "dengue", "malaria", "typhoid", "sugar", "diabetes", "bp", "blood",
            "report", "prescription", "diagnosis"
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
            
        # Instead of calling LLM synchronously, do a simple keyword matching score fallback
        text_lower = text.lower()
        
        # Scoring domains
        med_score = sum(1 for k in ["medical", "health", "hospital", "doctor", "medicine", "dawa", "bukhar", "pain", "treatment", "symptom", "hernia", "diseas", "tb", "fever"] if k in text_lower)
        leg_score = sum(1 for k in ["legal", "law", "court", "fir", "police", "rti", "rights", "kanoon", "dhara", "ipc", "crpc", "bnss", "constitution", "rule", "act"] if k in text_lower)
        bank_score = sum(1 for k in ["banking", "bank", "kyc", "account", "loan", "interest", "savings", "paisa", "card", "rbi", "prepayment", "foreclosure"] if k in text_lower)
        
        domain = "General"
        if med_score > 0 and med_score >= leg_score and med_score >= bank_score:
            domain = "Medical"
        elif leg_score > 0 and leg_score >= med_score and leg_score >= bank_score:
            domain = "Legal"
        elif bank_score > 0 and bank_score >= med_score and bank_score >= leg_score:
            domain = "Banking"
            
        return {
            "language": lang,
            "domain": domain,
            "intent": "QA",
            "confidence_score": 0.7,
            "query_type": "Domain_QA"
        }

intent_service = IntentService()
