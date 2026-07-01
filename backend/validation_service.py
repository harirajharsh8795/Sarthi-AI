import re
import logging
from config import settings

logger = logging.getLogger("saarthi.validation")

class ValidationService:
    """
    Implements a sentence-level Citation Validator and an AI Self-Evaluation checker.
    Cross-checks LLM response sentences against source context chunks to verify grounding.
    """

    def split_into_sentences(self, text: str) -> list:
        """Splits text into standalone sentences cleanly."""
        if not text:
            return []
        # Split by periods, question marks, exclamation marks followed by spaces or newlines
        sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
        return [s.strip() for s in sentences if s.strip()]

    def extract_nouns_and_numbers(self, text: str) -> set:
        """Extracts key nouns/numbers from text for token intersection matching."""
        # Simple extraction of capitalized words, numbers, and long tokens
        tokens = re.findall(r'\b\w+\b', text)
        keywords = set()
        for t in tokens:
            t_clean = t.strip()
            if t_clean.isdigit() or len(t_clean) >= 4:
                keywords.add(t_clean.lower())
        return keywords

    def validate_citations(self, answer: str, chunks: list) -> dict:
        """
        Citation Validator: Parses sentences and checks if assertions are supported by source chunks.
        If a sentence cites e.g. [1], it checks chunk 1 text specifically.
        Returns: {
            "validated_answer": str,
            "grounding_score": float,
            "unsupported_sentences": list
        }
        """
        sentences = self.split_into_sentences(answer)
        if not sentences:
            return {"validated_answer": answer, "grounding_score": 1.0, "unsupported_sentences": []}

        validated_sentences = []
        unsupported = []
        supported_count = 0

        # Map chunks by index
        chunk_map = {}
        for c in chunks:
            idx = c.get("index") or c.get("citation_indices", [1])[0]
            chunk_map[idx] = c["text"]

        for s in sentences:
            # Skip signature blocks
            if s.startswith("Sources:") or s.startswith("[") and ":" in s:
                validated_sentences.append(s)
                continue
                
            # Extract citations: e.g. [1], [2]
            citations = [int(n) for n in re.findall(r'\[(\d+)\]', s)]
            
            is_supported = False
            
            if citations:
                # Check cited chunks specifically
                for cit in citations:
                    if cit in chunk_map:
                        chunk_text = chunk_map[cit]
                        overlap = self.extract_nouns_and_numbers(s).intersection(self.extract_nouns_and_numbers(chunk_text))
                        # If we have keyword overlap, it is grounded
                        if len(overlap) >= 1 or len(chunk_text) < 50:
                            is_supported = True
                            break
            else:
                # No citations: Check overlap against ALL chunks
                for idx, chunk_text in chunk_map.items():
                    overlap = self.extract_nouns_and_numbers(s).intersection(self.extract_nouns_and_numbers(chunk_text))
                    if len(overlap) >= 2:
                        is_supported = True
                        break

            if is_supported or len(s.split()) <= 3:
                # Sentence is grounded, keep it
                supported_count += 1
                validated_sentences.append(s)
            else:
                # Unsupported claim
                unsupported.append(s)
                # We append a warning tag instead of completely deleting, to preserve layout
                validated_sentences.append(f"{s} [⚠️ Claim Unsupported by Sources]")

        grounding_score = supported_count / len(sentences) if sentences else 1.0
        validated_answer = " ".join(validated_sentences)
        
        logger.info(f"Citation validation complete. Grounding score={grounding_score:.2f}")
        return {
            "validated_answer": validated_answer,
            "grounding_score": round(grounding_score, 4),
            "unsupported_sentences": unsupported
        }

    def evaluate_response_self(self, answer: str, chunks: list, grounding_score: float) -> dict:
        """
        AI Self-Evaluation: Computes grounding, citation completion, missing info markers,
        and final hallucination risk metrics.
        """
        # Count citation counts in output
        citations = re.findall(r'\[\d+\]', answer)
        citations_complete = len(citations) > 0
        
        # Check if LLM response indicates missing info
        missing_phrases = ["cannot find", "not found", "insufficient evidence", "do not have information", "जानकारी नहीं मिली"]
        answer_lower = answer.lower()
        has_missing_info = any(phrase in answer_lower for phrase in missing_phrases)

        # Hallucination Risk Classification
        if grounding_score >= 0.85:
            risk = "Low"
        elif grounding_score >= 0.60:
            risk = "Medium"
        else:
            risk = "High"

        eval_summary = (
            f"Grounding={grounding_score*100:.1f}%, Citations={len(citations)}, "
            f"MissingInfo={has_missing_info}, Risk={risk}"
        )

        return {
            "grounding_score": grounding_score,
            "citations_complete": citations_complete,
            "has_missing_info": has_missing_info,
            "hallucination_risk": risk,
            "eval_summary": eval_summary
        }

validation_service = ValidationService()
