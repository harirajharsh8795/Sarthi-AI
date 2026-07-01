import re
import logging

logger = logging.getLogger("saarthi.security.prompt")

class PromptGuard:
    """
    Scans incoming queries to detect prompt injection, instruction hijacking,
    system prompt leakages, and jailbreak attempts.
    """
    
    def __init__(self):
        # Compiled regex vectors for threat vectors
        self.jailbreak_patterns = [
            r"\bignore\b.*\bprevious\b",
            r"\bignore\b.*\binstructions\b",
            r"\bsystem\s*prompt\b",
            r"\byou\s*are\s*no\s*longer\b",
            r"\bdo\s*anything\s*now\b",
            r"\bjailbreak\b",
            r"\bunder\s*what\s*conditions\b.*\bsystem\b",
            r"\bstart\s*response\s*with\b",
            r"\bhijack\b",
            r"\bdeveloper\s*mode\b",
            r"\bplease\s*leak\b"
        ]

    def scan_query(self, query: str) -> dict:
        """
        Scans a query and assigns Threat Score & Risk Level.
        Returns: {blocked: bool, reason: str, risk_level: str, rule_triggered: str}
        """
        if not query:
            return {"blocked": False, "reason": "", "risk_level": "Low", "rule_triggered": ""}

        query_lower = query.lower()
        
        # Check patterns
        for pattern in self.jailbreak_patterns:
            if re.search(pattern, query_lower):
                logger.warning(f"Prompt injection pattern detected: '{pattern}'")
                return {
                    "blocked": True,
                    "reason": "Instruction hijacking or system prompt leakage attempt detected.",
                    "risk_level": "High",
                    "rule_triggered": pattern
                }
                
        # Substring indicators (e.g. system prompt instructions)
        if "ignore the above" in query_lower or "ignore previous" in query_lower:
            return {
                "blocked": True,
                "reason": "Jailbreak bypass context override attempt.",
                "risk_level": "High",
                "rule_triggered": "context_override"
            }

        return {
            "blocked": False,
            "reason": "",
            "risk_level": "Low",
            "rule_triggered": ""
        }

prompt_guard = PromptGuard()
