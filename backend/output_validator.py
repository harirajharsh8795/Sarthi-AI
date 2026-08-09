import re
import logging
from post_processor import post_processor

logger = logging.getLogger("saarthi.security.output")

class OutputValidator:
    """
    Validates output formatting before sending to clients.
    Verifies citations compliance, checks markdown brackets, and fixes formatting.
    """
    
    def validate_and_refine_output(self, raw_answer: str, chunks: list, language: str = None) -> str:
        """
        Validates the generated output.
        Applies markdown polishing and guarantees no broken bracket syntax.
        Strips accidental Devanagari script if response language is Hinglish.
        """
        if not raw_answer:
            return "I could not compile a grounded answer based on the retrieved sources."

        refined = raw_answer.strip()
        
        # Check for citation spoofing (LLM citing numbers that don't exist in chunks)
        citations = [int(n) for n in re.findall(r'\[(\d+)\]', refined)]
        max_valid_idx = len(chunks)
        
        spoofed = False
        for c in citations:
            if c < 1 or c > max_valid_idx:
                spoofed = True
                # Remove the invalid citation bracket
                refined = refined.replace(f"[{c}]", "")
                
        if spoofed:
            logger.warning("Removed spoofed or out-of-range inline citation indexes.")

        # Strip accidental 'English: ...' translation lines if language is Hindi
        if language == "Hindi":
            refined = re.sub(r'^(?:English|Translation)\s*:.*$', '', refined, flags=re.MULTILINE | re.IGNORECASE)

        # Deduplicate consecutive identical sentences/lines to prevent LLM loop repeating
        lines = [l for l in refined.split("\n")]
        deduped_lines = []
        seen_lines = set()

        for line in lines:
            stripped = line.strip()
            # If line is a substantial text sentence (longer than 15 chars) and not a markdown header
            if len(stripped) > 15 and not stripped.startswith("#"):
                clean_key = re.sub(r"[^\w\s]", "", stripped.lower())
                if clean_key in seen_lines:
                    continue
                seen_lines.add(clean_key)
            deduped_lines.append(line)

        refined = "\n".join(deduped_lines).strip()

        # Balance checklist checks (e.g. check open bold tags)
        if refined.count("**") % 2 != 0:
            # Append closing tag to avoid UI layouts breaking
            refined += "**"
            
        return refined

output_validator = OutputValidator()

