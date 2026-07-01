import re
import json
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.followup")

class FollowupService:
    """
    Generates 3-5 relevant, contextual follow-up questions
    based on the conversation history and domain context.
    """

    def generate_followup_rules(self, domain: str, language: str) -> list:
        """Returns standard relevant suggestions based on domain fallback rules."""
        if language == "Hindi":
            if domain == "Medical":
                return [
                    "इस बीमारी के मुख्य लक्षण क्या हैं?",
                    "इसके लिए क्या प्राथमिक उपचार किया जाना चाहिए?",
                    "मुझे किस डॉक्टर से संपर्क करना चाहिए?"
                ]
            elif domain == "Legal":
                return [
                    "RTI आवेदन पत्र कैसे लिखें?",
                    "इसके लिए आवश्यक सरकारी दस्तावेज कौन से हैं?",
                    "क्या इसके खिलाफ अपील दायर की जा सकती है?"
                ]
            elif domain == "Banking":
                return [
                    "इसके लिए कौन से KYC दस्तावेज मान्य हैं?",
                    "खाता अपडेट होने में कितना समय लगता है?",
                    "RBI की शिकायत दर्ज करने की प्रक्रिया क्या है?"
                ]
        else: # English
            if domain == "Medical":
                return [
                    "What are the main symptoms of this condition?",
                    "What first aid measures should be taken?",
                    "Are there any side effects to the standard medication?"
                ]
            elif domain == "Legal":
                return [
                    "How do I file an appeal under this section?",
                    "What documents are required to file a complaint?",
                    "Is there a template available for this application?"
                ]
            elif domain == "Banking":
                return [
                    "What is the eligibility criteria for this account?",
                    "What official documents are accepted for KYC?",
                    "How do I report unauthorized transaction issues?"
                ]
                
        return [
            "Can you explain this in detail?",
            "What are the next steps to apply?",
            "What official documents are needed?"
        ]

    def generate_followups(self, query: str, answer: str, domain: str, language: str) -> list:
        """
        Generates 3-5 follow-up questions.
        Uses rule-based fallbacks or lightweight LLM calls.
        """
        # Call local LLM to generate highly contextual follow-ups
        prompt = (
            f"User Query: \"{query}\"\n"
            f"Answer: \"{answer[:500]}\"\n"
            f"Domain: {domain}\n"
            f"Language: {language}\n\n"
            f"Generate 3 short, relevant, and conversation-aware follow-up questions that the user might want to ask next. "
            f"Respond in the same language. Output ONLY a JSON list of strings, for example: "
            f"[\"question 1?\", \"question 2?\", \"question 3?\"]\n"
            f"Do not write conversational text or wrapper, output ONLY the JSON list."
        )

        try:
            r = requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": settings.LLM_MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=5
            )
            if r.status_code == 200:
                resp = r.json().get("response", "").strip()
                json_match = re.search(r'\[.*\]', resp, re.DOTALL)
                if json_match:
                    questions = json.loads(json_match.group(0))
                    if isinstance(questions, list) and len(questions) >= 2:
                        logger.info(f"Generated follow-up questions: {questions}")
                        return questions[:4]
        except Exception as e:
            logger.warning(f"Failed to generate follow-up questions via LLM: {e}")
            
        # Return fallback rule list
        return self.generate_followup_rules(domain, language)

followup_service = FollowupService()
