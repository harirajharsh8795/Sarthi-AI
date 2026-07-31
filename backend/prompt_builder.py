import logging

logger = logging.getLogger("saarthi.prompt")

# Internal-only Hinglish decode map — used to translate query before answering.
# The LLM should NEVER output these Hindi romanized words back to the user.
_HINGLISH_DECODE = {
    "pet dard": "stomach pain",
    "pet drd": "stomach pain",
    "pait dard": "stomach pain",
    "sir dard": "headache",
    "seena dard": "chest pain",
    "pet me jalan": "acidity / stomach burning",
    "dva": "medicine",
    "dvai": "medicine",
    "dawa": "medicine",
    "dawai": "medicine",
    "dava": "medicine",
    "dawaii": "medicine",
    "bukhar": "fever",
    "bhukar": "fever",
    "bukhr": "fever",
    "ulti": "vomiting",
    "khansi": "cough",
    "khaansi": "cough",
    "ilaj": "treatment",
    "upchar": "treatment",
    "ilaaj": "treatment",
    "bimari": "illness",
    "bimaari": "illness",
    "lakshan": "symptoms",
    "laksan": "symptoms",
    "btao": "tell me",
    "batao": "tell me",
    "btayie": "tell me",
    "batayie": "tell me",
}

def _decode_hinglish_query(query: str) -> str:
    """Silently decode Hinglish medical query into plain English for LLM understanding."""
    q = query.lower()
    for hindi, english in _HINGLISH_DECODE.items():
        q = q.replace(hindi, english)
    return q


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
        Builds system instructions, context chunks, and formatting rules.
        """

        # ── Silently decode Hinglish query into English so the LLM understands intent
        decoded_query = _decode_hinglish_query(query) if language == "Hinglish" else query

        # ── 1. Language instruction
        if language == "Hindi":
            lang_instruction = (
                "CRITICAL LANGUAGE RULE: Respond ONLY in Hindi using Devanagari script (हिंदी). "
                "Do NOT use English or Hinglish."
            )
        elif language == "Hinglish":
            lang_instruction = (
                "CRITICAL LANGUAGE RULE: Write your answer ONLY in natural, friendly Hinglish "
                "(conversational Hindi sentences using the English/Latin alphabet). "
                "Write like a helpful friend explaining things simply. "
                "IMPORTANT: Do NOT copy or echo the user's exact query words into every sentence. "
                "Do NOT repeat phrases like 'pet dard ki dva btao' in the answer — "
                "instead use natural phrases like 'stomach pain ke liye' or 'pet dard mein aaram ke liye'. "
                "Do NOT use Devanagari script and do NOT respond in plain English."
            )
        else:
            lang_instruction = "CRITICAL LANGUAGE RULE: Respond ONLY in clear, professional English."

        system_role = (
            "You are Saarthi AI, a helpful, caring, and accurate medical, legal, and banking assistant. "
            "You answer in a natural, human-friendly way — like a knowledgeable friend, not a robot.\n"
            f"{lang_instruction}\n"
        )

        # ── 2. Core answer rules
        rules = (
            "CORE RULES:\n"
            "1. Give a clear, natural, human-friendly answer. Do NOT be robotic or repetitive.\n"
            "2. NEVER repeat the user's original query words in every line of your answer.\n"
            "3. Do NOT mention 'Source Excerpts', 'Reference Facts', 'provided documents' or 'context'. "
            "Speak directly and naturally.\n"
            "4. Never refuse valid medical, legal, or banking questions.\n"
            "5. ANTI-HALLUCINATION: Only use information from the Reference Facts. "
            "Do NOT invent or assume anything not written there.\n"
        )

        # ── 3. User document directive
        has_user_doc = any(
            (c.get("collection") == "user_docs") or (c.get("domain") == "user_upload")
            for c in chunks
        ) if chunks else False

        if has_user_doc:
            heading_hint = (
                "(e.g., ### 📌 Report Summary, ### 📋 Patient Details, "
                "### 🔬 Test Results, ### 💡 Key Takeaways)"
            )
            doc_directive = (
                "DOCUMENT ANALYSIS RULES — FOLLOW WITHOUT EXCEPTION:\n"
                "The text below (in Reference Facts) is OCR-extracted from the uploaded document. "
                "Some words may be slightly garbled due to scan quality — use context to understand them.\n"
                "CRITICAL RULES:\n"
                "1. Extract and report ONLY what is actually written in the document. Never invent data.\n"
                "2. 'NON REACTIVE' = NEGATIVE. The patient does NOT have that condition. "
                "NEVER call a NON REACTIVE result 'positive'. Always write: ✅ NON REACTIVE (Negative).\n"
                "3. Read patient name, bill number, dates, test results EXACTLY as shown in the text. "
                "Common OCR garbling: 'SANICSM DEVE' likely means 'SANTOSH DEVI' — use best-effort reading.\n"
                "4. For each test in the report, clearly show: Test Name → Result.\n"
                "5. If something is genuinely not readable or missing, write: 'Not clearly readable in the scan'.\n"
                "6. Do NOT add any diagnosis, interpretation, or medical advice beyond what the report states.\n\n"
            )
        else:
            heading_hint = "(e.g., ### 📌 Overview, ### 💊 Medicines, ### ⚠️ When to See a Doctor)"
            doc_directive = ""

        # ── 4. Formatting rules
        formatting = (
            "FORMATTING RULES:\n"
            "- Use clean Markdown. Start with a 1-2 sentence plain overview.\n"
            f"- Use section headings like {heading_hint}.\n"
            "- Use **bold** for key terms, medicine names, test results, or important warnings.\n"
            "- Use bullet points for lists. Keep it concise and easy to read.\n"
            "- Sound natural and friendly, not clinical or repetitive.\n"
        )

        # ── 5. Context block — use decoded query as the framing question for the LLM
        if chunks:
            context_block = "Reference Facts (from the document / knowledge base):\n"
            for idx, c in enumerate(chunks, 1):
                context_block += f"Fact [{idx}]: {c['text']}\n\n"
        else:
            context_block = (
                "Reference Facts: No document match found. "
                "Answer using your general medical/legal/banking knowledge.\n\n"
            )

        # Show the decoded query to the LLM so it understands intent, but also show original query
        if language == "Hinglish" and decoded_query != query:
            user_block = (
                f"User's Question (original): {query}\n"
                f"Interpreted Meaning: {decoded_query}\n\n"
                f"Answer (in natural Hinglish):"
            )
        else:
            user_block = f"User Question: {query}\n\nAnswer:"

        full_prompt = (
            f"{system_role}\n"
            f"{rules}\n"
            f"{formatting}\n"
            f"{doc_directive}"
            f"{context_block}"
            f"{user_block}"
        )

        logger.info("Adaptive prompt constructed successfully.")
        return full_prompt


prompt_builder = PromptBuilder()
