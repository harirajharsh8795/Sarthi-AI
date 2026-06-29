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

        # Call local LLM to get a structured task decomposition plan
        prompt = (
            f"Query: \"{query}\"\n\n"
            f"Decompose the query above into a list of sub-questions/tasks for a document search engine. "
            f"Output JSON list containing exactly the keys: \"task_id\" (integer), "
            f"\"description\" (short detail of the task), and \"query_terms\" (standalone keywords to search). "
            f"Do not write conversational text or wrapper, output ONLY the JSON list."
        )

        try:
            r = requests.post(
                settings.OLLAMA_URL,
                json={
                    "model": settings.LLM_MODEL_NAME,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.0}
                },
                timeout=8
            )
            if r.status_code == 200:
                resp = r.json().get("response", "").strip()
                json_match = re.search(r'\[.*\]', resp, re.DOTALL)
                if json_match:
                    plan = json.loads(json_match.group(0))
                    if isinstance(plan, list) and len(plan) > 0:
                        logger.info(f"Generated query plan: {plan}")
                        return plan
        except Exception as e:
            logger.warning(f"Failed to generate query plan using LLM: {e}")

        # Fallback to simple split
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
