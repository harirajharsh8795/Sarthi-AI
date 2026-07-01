import logging

logger = logging.getLogger("saarthi.confidence")

class ConfidenceService:
    """
    Computes a multi-factor confidence rating for RAG pipeline inferences.
    Considers similarity scores, source trust ratings, citation counts, and domain match.
    """

    def calculate_confidence(
        self, 
        chunks: list, 
        query_domain: str, 
        citations_used_count: int,
        skipped_llm: bool = False
    ) -> dict:
        """
        Calculates calibrated confidence score (0-100%) and returns status labels.
        """
        if skipped_llm:
            return {
                "confidence_score": 0.0,
                "confidence_label": "No Confidence",
                "reason": "Query fell below relevance threshold. Skyped LLM generation."
            }

        if not chunks:
            return {
                "confidence_score": 0.0,
                "confidence_label": "No Confidence",
                "reason": "No evidence retrieved."
            }

        # 1. Similarity factor (max and avg)
        similarities = [c.get("similarity_score", c.get("hybrid_score", 0.0)) for c in chunks]
        max_sim = max(similarities) if similarities else 0.0
        avg_sim = sum(similarities) / len(similarities) if similarities else 0.0
        
        # 2. Source trust factor
        trust_scores = [c.get("trust_score", 0.90) for c in chunks]
        avg_trust = sum(trust_scores) / len(trust_scores) if trust_scores else 0.90

        # 3. Domain match check
        domain_matches = sum(1 for c in chunks if str(c.get("domain", "")).lower() == query_domain.lower())
        domain_match_ratio = domain_matches / len(chunks) if chunks else 0.0

        # 4. Evidence count factor (more chunks increase confidence, caps at 5)
        evidence_count_factor = min(1.0, len(chunks) / 5.0)

        # 5. Citation coverage factor (how many of our chunks were cited in final response)
        citation_factor = min(1.0, (citations_used_count / len(chunks))) if chunks else 0.0

        # Calibration formula
        # 40% similarity + 20% trust + 15% domain match + 15% citation usage + 10% evidence quantity
        score = (
            (max_sim * 0.40) + 
            (avg_trust * 0.20) + 
            (domain_match_ratio * 0.15) + 
            (citation_factor * 0.15) + 
            (evidence_count_factor * 0.10)
        )
        
        score_pct = round(score * 100.0, 2)
        
        # Assign label and reasoning
        if score_pct >= 85:
            label = "High Confidence"
            reason = "Multiple highly relevant and trusted official sources support this answer."
        elif score_pct >= 60:
            label = "Medium Confidence"
            reason = "Supporting evidence retrieved, but sources have moderate matching features."
        else:
            label = "Low Confidence"
            reason = "Retrieved evidence has low similarity or trust alignment. Hallucination risk."

        logger.info(f"Calibrated confidence: {score_pct}% ({label}) - {reason}")
        
        return {
            "confidence_score": score_pct,
            "confidence_label": label,
            "reason": reason
        }

confidence_service = ConfidenceService()
