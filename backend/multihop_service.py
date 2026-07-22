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
        conversation_id: str = None,
        query_language: str = None,
        original_query: str = None
    ) -> list:
        """
        Runs a retrieval query for each task in the query plan and merges results.
        Enforces deduplication of chunks by source and page.
        """
        # If the original query or plan concerns user documents, bypass multi-hop
        is_doc_query = False
        if original_query and retrieval_router.is_document_about_query(original_query):
            is_doc_query = True
        elif query_plan and any(retrieval_router.is_document_about_query(t.get("query_terms", "") or t.get("description", "")) for t in query_plan):
            is_doc_query = True

        if is_doc_query:
            sub_query = original_query or (query_plan[0].get("query_terms") or query_plan[0].get("description") if query_plan else "")
            logger.info(f"Document query detected. Bypassing multi-hop retrieval for: '{sub_query}'")
            res = retrieval_router.retrieve_context(sub_query, session_id, conversation_id, query_language=query_language)
            chunks = res.get("context_chunks", [])
            return ranking_service.rerank_chunks(sub_query, chunks)

        all_chunks = []
        seen_identifiers = set()
        
        # Limit to max 3 hops to prevent latency explosion
        tasks_to_run = query_plan[:3]
        
        for task in tasks_to_run:
            sub_query = task.get("query_terms") or task.get("description")
            logger.info(f"Triggering RAG hop for sub-task query: '{sub_query}'")
            
            # Run sub-query retrieval
            res = retrieval_router.retrieve_context(sub_query, session_id, conversation_id, query_language=query_language)
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
