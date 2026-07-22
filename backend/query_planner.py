import re
import json
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.planner")

class QueryPlanner:
    """
    Decomposes compound or multi-intent user queries into discrete sub-queries/tasks.
    Allows RAG pipeline to pull precise evidence for each sub-topic.
    """
    
    def plan_query(self, query: str) -> list:
        """
        Decomposes query into a list of tasks.
        Returns a list of dicts: [{"task_id": int, "description": str, "query_terms": str}]
        """
        query_lower = query.lower()
        
        # Simple regex split check for compound questions using coordinating conjunctions
        conjunctions = [r"\band\b", r"\baur\b", r"\bas well as\b", r"\bsath hi\b", r"\bke sath\b"]
        split_pattern = "|".join(conjunctions)
        
        # Check if we should split
        has_conjunction = any(re.search(pat, query_lower) for pat in conjunctions)
        
        if not has_conjunction or len(query.split()) < 6:
            # Simple single-topic query
            return [{
                "task_id": 1,
                "description": f"Retrieve and explain info for: {query}",
                "query_terms": query
            }]

        # To minimize pre-generation latency on local 1B model, bypass LLM planner and use simple regex split fallback directly
        parts = re.split(split_pattern, query, flags=re.IGNORECASE)
        plan = []
        for idx, part in enumerate(parts, 1):
            clean_part = part.strip()
            if len(clean_part) > 3:
                plan.append({
                    "task_id": idx,
                    "description": f"Verify: {clean_part}",
                    "query_terms": clean_part
                })
        return plan if plan else [{"task_id": 1, "description": f"Explain: {query}", "query_terms": query}]

query_planner = QueryPlanner()
