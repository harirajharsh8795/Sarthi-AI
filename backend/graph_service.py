import re
import json
import logging
import requests
from config import settings

logger = logging.getLogger("saarthi.graph")

class GraphService:
    """
    Extracts Entity-Relation-Entity (Subject, Predicate, Object) triplets
    from document chunks or query texts to form a JSON Knowledge Graph.
    """
    
    def clean_token(self, token: str) -> str:
        return re.sub(r'[^\w\s-]', '', token).strip()

    def extract_graph_regex(self, text: str) -> list:
        """Rule-based extraction for common legal/banking patterns."""
        triples = []
        
        # 1. "A requires B" pattern
        require_matches = re.finditer(
            r'\b([a-zA-Z\s]{2,20})\b\s+(?:requires|needs|compels|manga hai|chahiye)\s+\b([a-zA-Z\s]{2,20})\b', 
            text, re.IGNORECASE
        )
        for m in require_matches:
            sub = self.clean_token(m.group(1))
            obj = self.clean_token(m.group(2))
            if sub and obj:
                triples.append({"subject": sub, "relation": "requires", "object": obj})

        # 2. "A issues B" pattern
        issue_matches = re.finditer(
            r'\b([a-zA-Z\s]{2,20})\b\s+(?:issues|releases|publishes|lagu karta hai)\s+\b([a-zA-Z\s]{2,20})\b', 
            text, re.IGNORECASE
        )
        for m in issue_matches:
            sub = self.clean_token(m.group(1))
            obj = self.clean_token(m.group(2))
            if sub and obj:
                triples.append({"subject": sub, "relation": "issues", "object": obj})

        # 3. "A is a B" pattern
        is_matches = re.finditer(
            r'\b([a-zA-Z\s]{2,20})\b\s+(?:is a|is an|ek type hai|hai)\s+\b([a-zA-Z\s]{2,20})\b', 
            text, re.IGNORECASE
        )
        for m in is_matches:
            sub = self.clean_token(m.group(1))
            obj = self.clean_token(m.group(2))
            if sub and obj:
                triples.append({"subject": sub, "relation": "is_a", "object": obj})
                
        return triples

    def extract_knowledge_graph(self, text: str, use_llm: bool = True) -> list:
        """
        Extracts up to 5 key entity-relation triples from a text block.
        Returns a list of dicts: [{"subject": "...", "relation": "...", "object": "..."}]
        """
        # Run regex rules first
        regex_triples = self.extract_graph_regex(text)
        if len(regex_triples) >= 3:
            return regex_triples[:5]
            
        if not use_llm:
            return regex_triples

        # Fallback to local Ollama model to pull complex relations
        prompt = (
            f"Text: \"{text[:1000]}\"\n\n"
            f"Extract up to 4 key Entity-Relation-Entity triplets from the text above. "
            f"Output JSON list containing exactly the keys: \"subject\", \"relation\", and \"object\". "
            f"Return ONLY the JSON list. Do not write conversational wrapper."
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
                    triples = json.loads(json_match.group(0))
                    if isinstance(triples, list):
                        # Merge lists
                        merged = regex_triples + triples
                        # Unique check
                        unique = []
                        seen = set()
                        for t in merged:
                            key = f"{t.get('subject')}_{t.get('relation')}_{t.get('object')}".lower()
                            if key not in seen:
                                seen.add(key)
                                unique.append(t)
                        logger.info(f"Knowledge Graph Triples extracted: {unique[:5]}")
                        return unique[:5]
        except Exception as e:
            logger.warning(f"Failed to extract knowledge graph via LLM: {e}")
            
        return regex_triples[:5]

graph_service = GraphService()
