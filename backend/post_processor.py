import re
import logging

logger = logging.getLogger("saarthi.postprocessor")

class PostProcessor:
    """
    Polishes final LLM outputs to guarantee correct markdown layout structure,
    proper bullet spacing, bold elements, and citation syntax.
    """

    def format_markdown(self, text: str) -> str:
        """Fixes layout spacings, cleans bullet points, and cleans citation syntax."""
        if not text:
            return ""

        # 1. Clean spacing around headings (##, ###)
        text = re.sub(r'\n*(##+)\s*(.*?)\n*', r'\n\n\1 \2\n\n', text)
        
        # 2. Fix malformed citation formatting (e.g., [ 1 ] or [citation 1])
        text = re.sub(r'\[\s*citation\s*(\d+)\s*\]', r'[\1]', text, flags=re.IGNORECASE)
        text = re.sub(r'\[\s*(\d+)\s*\]', r'[\1]', text)
        
        # 3. Clean spaces between citation numbers (e.g. [1] [2] -> [1][2])
        text = re.sub(r'\[(\d+)\]\s+\[(\d+)\]', r'[\1][2]', text)

        # 4. Standardize bullet point prefixes (* -> -)
        text = re.sub(r'^\s*\*\s+', r'- ', text, flags=re.MULTILINE)

        # 5. Fix double spaces or redundant newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        return text.strip()

post_processor = PostProcessor()
