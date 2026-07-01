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
        pronouns = {
            "it", "this", "that", "they", "them", "he", "she", "him", "her",
            "iska", "uske", "unka", "inhe", "unhe", "yeh", "woh", "what is this",
            "explain more", "samjhao", "bataye", "elaborate", "tell me more",
            "is eligible?", "how?", "kyu?", "kab?", "kahan?", "kya hai?"
        }
        
        # Check if query is short and contains pronouns or starts with triggers
        if len(text_lower.split()) <= 4:
            return True
            
        for p in pronouns:
            if p in text_lower:
                return True
                
        return False

    def rewrite_query(self, query: str, history: list) -> str:
        """
        Rewrites the query using history to maintain standby search relevance.
        history is a list of dicts: [{"role": "user"/"assistant", "content": "..."}]
        """
        if not history or not self.needs_rewrite(query):
            return query

        # Slice last 3 messages for concise history representation
        recent_history = history[-3:]
        history_str = ""
        for m in recent_history:
            role_label = "User" if m["role"] == "user" else "Assistant"
            history_str += f"{role_label}: {m['content']}\n"

        prompt = (
            f"Conversation history:\n{history_str}\n"
            f"User follow-up message: \"{query}\"\n\n"
            f"Given the conversation history above, rewrite the user's follow-up message into a complete, standalone question. "
            f"Ensure theStandalone Question contains all missing references (pronouns, subjects) and preserves the user's original language (e.g. English, Hindi, or Hinglish). "
            f"Do not add any additional information, explanations, or greeting wrapper. Return ONLY the rewritten question."
        )

        try:
            r = requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": settings.LLM_MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1}
                },
                timeout=8
            )
            if r.status_code == 200:
                rewritten = r.json().get("response", "").strip()
                # Clean quotes
                rewritten = re.sub(r'^["\']|["\']$', '', rewritten)
                if rewritten and len(rewritten.split()) > 1:
                    logger.info(f"Expanded query: '{query}' -> '{rewritten}'")
                    return rewritten
        except Exception as e:
            logger.warning(f"Failed to expand query via LLM: {e}")
            
        return query

rewrite_service = RewriteService()
