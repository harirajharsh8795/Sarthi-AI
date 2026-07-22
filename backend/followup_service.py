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
        Generates 3-4 follow-up questions rapidly using domain rule sets.
        """
        return self.generate_followup_rules(domain, language)

followup_service = FollowupService()
