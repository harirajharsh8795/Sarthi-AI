import logging
import retrieval_router
from ranking_service import ranking_service

logger = logging.getLogger("saarthi.multihop")

class MultihopService:
    """
    Coordinates multi-hop retrieval pipelines.
    Runs sequential searches for query plan sub-tasks to compile evidence.
    """
    
    def retrieve_multihop(
        self, 
        query_plan: list, 
        session_id: str, 
        conversation_id: str = None
    ) -> list:
        """
        Runs a retrieval query for each task in the query plan and merges results.
        Enforces deduplication of chunks by source and page.
        """
        all_chunks = []
        seen_identifiers = set()
        
        # Limit to max 3 hops to prevent latency explosion
        tasks_to_run = query_plan[:3]
        
        for task in tasks_to_run:
            sub_query = task.get("query_terms") or task.get("description")
            logger.info(f"Triggering RAG hop for sub-task query: '{sub_query}'")
            
            # Run sub-query retrieval
            res = retrieval_router.retrieve_context(sub_query, session_id, conversation_id)
            chunks = res.get("context_chunks", [])
            
            # Rerank retrieved chunks
            ranked_chunks = ranking_service.rerank_chunks(sub_query, chunks)
            
            for chunk in ranked_chunks:
                # Deduplication identifier: filename_pageNumber_textSnippetHash
                snippet = chunk["text"][:30]
                ident = f"{chunk['source']}_p{chunk['page_number']}_{hash(snippet)}"
                
                if ident not in seen_identifiers:
                    seen_identifiers.add(ident)
                    all_chunks.append(chunk)
                    
        logger.info(f"Multi-hop retrieval completed. Merged total unique chunks: {len(all_chunks)}")
        return all_chunks

multihop_service = MultihopService()
