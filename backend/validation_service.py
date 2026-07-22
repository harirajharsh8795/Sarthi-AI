import re
import logging
from config import settings

logger = logging.getLogger("saarthi.validation")

STOPWORDS = {
    "kya", "hai", "me", "mein", "se", "ko", "ne", "par", "pe", "ka", "ki", "ke", "jo", "aur", "ya", "toh", "tha", "thi", "the",
    "what", "how", "why", "who", "where", "when", "which", "is", "are", "am", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "a", "an", "the", "and", "or", "but", "if", "then", "else", "of", "at", "by", "for", "with", "about", "against",
    "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there", "all", "any", "both", "each", "few", "more", "most", "other",
    "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "should", "now"
}

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

    def validate_citations(self, answer: str, chunks: list, query: str = None) -> dict:
        """
        Citation Validator: Parses sentences and checks if assertions are supported by source chunks.
        If a sentence cites e.g. [1], it checks chunk 1 text specifically.
        Preserves the original markdown structure of the answer.
        Returns: {
            "validated_answer": str,
            "grounding_score": float,
            "unsupported_sentences": list
        }
        """
        # Split into sentences for grounding analysis, but keep the original text intact
        sentences = re.split(r'(?<=[.!?])\s+', answer.replace('\n', ' __NL__ '))
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return {"validated_text": answer, "validated_answer": answer, "grounding_score": 1.0, "unsupported_sentences": []}

        unsupported = []
        supported_count = 0

        # Extract query keywords
        query_words = set()
        if query:
            tokens = re.findall(r'\b\w+\b', query.lower())
            query_words = {t for t in tokens if len(t) >= 3 and t not in STOPWORDS}

        # Map chunks by index
        chunk_map = {}
        chunk_words_map = {}
        for c in chunks:
            idx = c.get("index") or c.get("citation_indices", [1])[0]
            chunk_text = c["text"]
            chunk_map[idx] = chunk_text
            chunk_words_map[idx] = {t.lower() for t in re.findall(r'\b\w+\b', chunk_text.lower())}

        validated_sentences = []
        for s in sentences:
            clean_s = s.replace(' __NL__ ', ' ')
            if clean_s.startswith("Sources:") or clean_s.startswith("[") and ":" in clean_s:
                supported_count += 1
                validated_sentences.append(s)
                continue
                
            citations = [int(n) for n in re.findall(r'\[(\d+)\]', clean_s)]
            sentence_words = {t.lower() for t in re.findall(r'\b\w+\b', clean_s.lower())}
            is_supported = False
            
            if citations:
                for cit in citations:
                    if cit in chunk_map:
                        chunk_text = chunk_map[cit]
                        chunk_words = chunk_words_map[cit]
                        
                        # Strict Query-Keyword match
                        query_words_in_sentence = query_words.intersection(sentence_words)
                        query_words_not_in_chunk = query_words_in_sentence.difference(chunk_words)
                        if len(query_words_not_in_chunk) > 0:
                            continue
                            
                        overlap = self.extract_nouns_and_numbers(clean_s).intersection(self.extract_nouns_and_numbers(chunk_text))
                        if len(overlap) >= 1 or len(chunk_text) < 50:
                            is_supported = True
                            break
            else:
                for idx, chunk_text in chunk_map.items():
                    chunk_words = chunk_words_map[idx]
                    
                    query_words_in_sentence = query_words.intersection(sentence_words)
                    query_words_not_in_chunk = query_words_in_sentence.difference(chunk_words)
                    if len(query_words_not_in_chunk) > 0:
                        continue
                        
                    overlap = self.extract_nouns_and_numbers(clean_s).intersection(self.extract_nouns_and_numbers(chunk_text))
                    if len(overlap) >= 2:
                        is_supported = True
                        break

            if is_supported or len(clean_s.split()) <= 3:
                supported_count += 1
                validated_sentences.append(s)
            else:
                unsupported.append(clean_s)
                validated_sentences.append(s)

        validated_answer = " ".join(validated_sentences).replace(' __NL__ ', '\n')
        grounding_score = supported_count / len(sentences) if sentences else 1.0
        
        logger.info(f"Citation validation complete. Grounding score={grounding_score:.2f}")
        return {
            "validated_text": validated_answer,
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
