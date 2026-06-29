import logging

logger = logging.getLogger("saarthi.prompt")

class PromptBuilder:
    """
    Constructs highly optimized, domain-specific, and language-tailored RAG prompts
    specifically tuned for lightweight local models (llama3.2:1b).
    """

    def build_adaptive_prompt(
        self, 
        query: str, 
        chunks: list, 
        language: str, 
        domain: str, 
        intent: str, 
        query_plan: list = None,
        graph_triples: list = None
    ) -> str:
        """
        Builds the system instructions, context chunks, query plan, and user question blocks.
        """
        # 1. System instructions block
        system_role = (
            f"You are Saarthi AI, a trusted cognitive offline assistant specializing in Indian {domain.lower()} domains.\n"
            f"Your language of response MUST be: {language}.\n"
        )
        
        # 2. Strict grounding constraints
        constraints = (
            "CRITICAL: Answer the query using ONLY the provided Source Excerpts below. Do NOT use external assumptions.\n"
            "If the source excerpts do not contain the answer, explicitly state that you cannot find the answer in the provided documents.\n"
        )

        # 3. Inject Knowledge Graph Context (if available)
        graph_block = ""
        if graph_triples:
            graph_block = "Structured Entity-Relations:\n"
            for t in graph_triples:
                graph_block += f"- ({t.get('subject')}) --[{t.get('relation')}]--> ({t.get('object')})\n"
            graph_block += "\n"

        # 4. Context chunks assembly
        context_block = "Source Excerpts:\n"
        for c in chunks:
            indices_str = ",".join(map(str, c.get("citation_indices", [c.get("index", 1)])))
            context_block += (
                f"[{indices_str}] Source: {c['source']}, Page {c['page_number']} "
                f"({c.get('domain', 'general')})\n{c['text']}\n\n"
            )

        # 5. Citation layout instructions
        citation_rules = (
            "Format inline citations using the exact source number bracket, e.g. [1] or [2].\n"
            "At the end of your answer, list all cited sources under a 'Sources:' heading, e.g.:\n"
            "Sources:\n"
        )
        # Generate citation definitions dynamically
        seen_indices = set()
        for c in chunks:
            indices = c.get("citation_indices", [c.get("index", 1)])
            for idx in indices:
                if idx not in seen_indices:
                    seen_indices.add(idx)
                    citation_rules += f"[{idx}] {c['source']}, Page {c['page_number']}\n"

        # 6. Query Plan block (to guide LLM's logical flow)
        plan_block = ""
        if query_plan and len(query_plan) > 1:
            plan_block = "Logical Query Plan Tasks:\n"
            for t in query_plan:
                plan_block += f"- Task {t['task_id']}: {t['description']}\n"
            plan_block += "\n"

        # 7. Final user prompt
        user_block = f"Question: {query}\n\nAnswer:"

        # Combine all parts
        full_prompt = (
            f"{system_role}\n"
            f"{constraints}\n"
            f"{graph_block}"
            f"{context_block}"
            f"{citation_rules}\n"
            f"{plan_block}"
            f"{user_block}"
        )
        
        logger.info("Adaptive prompt constructed successfully.")
        return full_prompt

prompt_builder = PromptBuilder()
