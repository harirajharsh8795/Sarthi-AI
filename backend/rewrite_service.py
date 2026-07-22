import re
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.rewrite")

class RewriteService:
    """
    Reformulates follow-up queries or ambiguous context statements
    into standalone search queries using conversation history.
    """
    
    def needs_rewrite(self, text: str) -> bool:
        """Determines if the query is a follow-up or highly context-dependent."""
        text_lower = text.lower().strip()
        pronouns_regex = [
            r"\b(it|this|that|they|them|he|she|him|her)\b",
            r"\b(iska|uske|unka|inhe|unhe|yeh|woh)\b",
            r"\b(samjhao|explain\s+more|tell\s+me\s+more)\b",
            r"\b(is\s+eligible\??|kyu\??|kab\??|kahan\??)\b",
            r"\b(translate\s+this|in\s+english|in\s+hindi|in\s+hinglish)\b"
        ]
        
        for pat in pronouns_regex:
            if re.search(pat, text_lower):
                return True
                
        return False

    def rewrite_query(self, query: str, history: list) -> str:
        """
        Rewrites context-dependent queries using conversation history.
        Uses fast heuristic matching to avoid blocking LLM timeouts.
        """
        if not history or not self.needs_rewrite(query):
            return query

        # Fast heuristic: if user asks for translation / clarification in short prompt, return last user query
        query_clean = query.lower().strip()
        words = re.findall(r'\b[a-zA-Z\u0900-\u097f]+\b', query_clean)
        pure_keywords = {
            "hinglish", "hindi", "english", "translate", "explain", "detail", "details", 
            "batao", "samjhao", "kro", "karo", "please", "more", "elaborate", "in", "me", 
            "se", "pe", "par", "plz", "cro", "caro", "explaination", "explanation"
        }
        if words and all(w in pure_keywords for w in words):
            for m in reversed(history[:-1]):
                if m.get("role") == "user" and m.get("content", "").strip():
                    logger.info(f"Heuristic query rewrite: '{query}' -> '{m['content']}'")
                    return m["content"]

        # Only append previous query context if query is very short (< 4 words) and context-dependent
        if len(words) <= 4:
            for m in reversed(history[:-1]):
                if m.get("role") == "user" and m.get("content", "").strip():
                    prev_text = m["content"].strip()
                    logger.info(f"Contextual query append: '{query}' -> '{prev_text} ({query})'")
                    return f"{prev_text} {query}"

        return query

rewrite_service = RewriteService()
