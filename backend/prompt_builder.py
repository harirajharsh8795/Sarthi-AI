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
        lang_instruction = ""
        if language == "Hindi":
            lang_instruction = "CRITICAL: You MUST reply entirely in Hindi using the Devanagari script. Do NOT use English or Hinglish."
        elif language == "Hinglish":
            lang_instruction = (
                "CRITICAL: You MUST reply entirely in Hinglish. Hinglish means writing Hindi words using ONLY the English/Latin alphabet. "
                "For example: 'Aapko fever ke liye paracetamol leni chahiye' or 'Mera bank account block ho gaya hai'. "
                "ABSOLUTELY DO NOT USE DEVANAGARI SCRIPT (like हिंदी) and DO NOT reply in plain English."
            )
        else:
            lang_instruction = "CRITICAL: You MUST reply entirely in English."

        system_role = (
            f"You are Saarthi AI, a trusted medical, legal, and banking cognitive offline assistant.\n"
            f"{lang_instruction}\n"
        )
        
        # 2. Strict grounding & topic focus constraints
        constraints = (
            "VERY IMPORTANT RULES:\n"
            "1. Answer the user's question directly, clearly, and completely using ONLY the facts in the Source Excerpts below.\n"
            "2. Always provide a full, helpful, and objective answer. Never refuse or decline to answer valid medical, legal, or banking queries.\n"
            "3. Stay strictly focused on the user's specific question. Do not bring up unrelated topics.\n"
            "4. Keep your answer clear, informative, and professional.\n"
        )

        # 2.5 Formatting instructions
        formatting = (
            "FORMAT YOUR ANSWER:\n"
            "- Write a complete, multi-sentence response in clean prose.\n"
            "- Use bullet points or numbered steps where helpful.\n"
            "- Do NOT output LaTeX math, boxed math, or raw code blocks.\n"
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
            is_user_upload = (c.get('collection') == 'user_docs') or (c.get('domain') == 'user_upload')
            priority_tag = " (Priority: HIGH - USER UPLOADED DOCUMENT)" if is_user_upload else ""
            
            context_block += (
                f"Excerpt [{indices_str}]{priority_tag}:\n{c['text']}\n\n"
            )

        # 5. Logical Query Plan block
        plan_block = ""
        if query_plan and len(query_plan) > 1:
            plan_block = "Logical Query Plan Tasks:\n"
            for t in query_plan:
                plan_block += f"- Task {t['task_id']}: {t['description']}\n"
            plan_block += "\n"

        # Check if user uploaded documents are present in chunks
        has_user_doc = any(
            (c.get('collection') == 'user_docs') or (c.get('domain') == 'user_upload') 
            for c in chunks
        )
        
        doc_access_directive = ""
        if has_user_doc:
            doc_access_directive = (
                "DOCUMENT ANALYSIS DIRECTIVE:\n"
                "The user has uploaded a document/image. The transcribed text of their document is provided below under 'Source Excerpts'. "
                "Analyze and summarize the Excerpts directly in clear, helpful prose. Start your response immediately with the document summary.\n\n"
            )

        # 7. Final user prompt
        user_block = f"Question: {query}\n\nAnswer:"

        # Combine all parts
        full_prompt = (
            f"{system_role}\n"
            f"{constraints}\n"
            f"{doc_access_directive}"
            f"{formatting}\n"
            f"{graph_block}"
            f"{context_block}"
            f"{user_block}"
        )
        
        logger.info("Adaptive prompt constructed successfully.")
        return full_prompt

prompt_builder = PromptBuilder()
