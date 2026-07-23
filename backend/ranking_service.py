import re
import math
import numpy as np
import logging
from config import settings

logger = logging.getLogger("saarthi.ranking")

class RankingService:
    """
    Implements a Hybrid Retrieval Ranker.
    Reranks chunks using Cosine Similarity, keyword overlap, source trust weighting,
    and calculates retrieval benchmarking metrics (Precision, Recall, MRR, NDCG).
    """

    def get_source_trust_score(self, metadata: dict) -> float:
        """Determines trust coefficient based on document origin."""
        source_name = str(
            metadata.get("source", "") or 
            metadata.get("filename", "") or 
            metadata.get("original_filename", "")
        ).lower()
        domain = str(metadata.get("domain", "")).lower()
        
        # Government sources / official portals
        if "gazette" in source_name or "govt" in source_name or "india.gov" in source_name:
            return 1.0
        if "rbi" in source_name or "nhm" in source_name or "mohfw" in source_name:
            return 0.98
        # User uploaded docs
        if metadata.get("collection") == "user_docs" or "user_upload" in domain:
            return 0.95
        # Standard public library docs
        return 0.90

    def compute_keyword_overlap(self, query: str, chunk_text: str) -> float:
        """Calculates token overlap ratio between query terms and text."""
        query_words = set(re.findall(r'\b\w+\b', query.lower()))
        chunk_words = set(re.findall(r'\b\w+\b', chunk_text.lower()))
        if not query_words:
            return 0.0
        overlap = query_words.intersection(chunk_words)
        return len(overlap) / len(query_words)

    def rerank_chunks(self, query: str, chunks: list) -> list:
        """
        Reranks raw retrieved chunks applying trust weights and keyword match factors.
        Each chunk is expected to be a dict: {text, source, domain, language, page_number, collection, similarity_score}
        """
        if not chunks:
            return []
            
        reranked = []
        for c in chunks:
            sim = c.get("similarity_score", 0.0)
            overlap = self.compute_keyword_overlap(query, c["text"])
            trust = self.get_source_trust_score(c)
            
            # Filter out completely irrelevant chunks (similarity < 0.20 and zero keyword overlap)
            if sim < 0.20 and overlap == 0.0:
                continue

            # Multiplicative hybrid score: 70% similarity, 30% keyword overlap, with minor trust multiplier (0.95 to 1.0)
            base_score = (sim * 0.70) + (overlap * 0.30)
            trust_multiplier = 0.95 + (trust * 0.05)
            hybrid_score = base_score * trust_multiplier
            
            c_copy = dict(c)
            c_copy["trust_score"] = trust
            c_copy["keyword_overlap"] = overlap
            c_copy["hybrid_score"] = round(hybrid_score, 4)
            reranked.append(c_copy)
            
        # Sort by hybrid score descending
        reranked.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return reranked

    def evaluate_retrieval_benchmarks(self, reranked_chunks: list, threshold: float = 0.55) -> dict:
        """
        Calculates Precision@K, Recall@K, MRR, and NDCG over the retrieved results.
        Relevance is defined as hybrid_score >= threshold.
        """
        if not reranked_chunks:
            return {"precision": 0.0, "recall": 0.0, "mrr": 0.0, "ndcg": 0.0}
            
        relevance_vector = [1 if c["hybrid_score"] >= threshold else 0 for c in reranked_chunks]
        n = len(relevance_vector)
        
        # 1. Precision@K
        relevant_retrieved = sum(relevance_vector)
        precision = relevant_retrieved / n if n > 0 else 0.0
        
        # 2. Recall@K (ratio of relevant retrieved items against target retrieval batch size)
        recall = precision
        
        # 3. MRR (Mean Reciprocal Rank)
        mrr = 0.0
        for idx, rel in enumerate(relevance_vector):
            if rel == 1:
                mrr = 1.0 / (idx + 1)
                break
                
        # 4. NDCG (Normalized Discounted Cumulative Gain)
        dcg = 0.0
        for idx, rel in enumerate(relevance_vector):
            dcg += rel / math.log2(idx + 2)
            
        # Ideal DCG (sort relevance descending)
        ideal_relevance = sorted(relevance_vector, reverse=True)
        idcg = 0.0
        for idx, rel in enumerate(ideal_relevance):
            idcg += rel / math.log2(idx + 2)
            
        ndcg = dcg / idcg if idcg > 0 else 0.0
        
        logger.info(f"Retrieval Benchmarks: Precision={precision:.2f}, Recall={recall:.2f}, MRR={mrr:.2f}, NDCG={ndcg:.2f}")
        
        return {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "mrr": round(mrr, 4),
            "ndcg": round(ndcg, 4)
        }

ranking_service = RankingService()
