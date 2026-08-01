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
                "(conversational Hindi sentences written using the English/Latin alphabet). "
                "Write like a helpful, caring friend explaining things simply and clearly. "
                "IMPORTANT DIRECTIVE: Answer ONLY the user's specific question based on the Reference Facts provided. "
                "NEVER mention or invent unrelated medical topics, symptoms, or diseases that are NOT present in the Reference Facts or user question. "
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
            "1. Give a clear, concise, natural, and human-friendly answer. Do NOT be robotic or repetitive.\n"
            "2. Answer STRICTLY about the topic asked in the user's query or reference facts. NEVER introduce unrelated diseases, organs, or symptoms.\n"
            "3. Do NOT mention 'Source Excerpts', 'Reference Facts', 'provided documents' or 'context'. Speak directly and naturally.\n"
            "4. Never refuse valid medical, legal, or banking questions.\n"
            "5. ACCURACY & FALLBACK: If Reference Facts are provided below, base your answer primarily on them and cite sources as [1], [2].\n"
            "6. CITATION FORMAT: Use citation brackets like [1], [2] at the end of sentences that use facts from Reference Facts.\n"
        )


        # ── 3. User document directive
        has_user_doc = any(
            (c.get("collection") == "user_docs") or (c.get("domain") == "user_upload")
            for c in chunks
        ) if chunks else False

        if has_user_doc:
            doc_directive = (
                "DOCUMENT REPORT EXTREMELY CRITICAL RULE:\n"
                "The text in Reference Facts below contains the EXACT OCR text of the user's uploaded document/image.\n"
                "1. STRICT FACTUAL GROUNDING: You MUST rely ONLY on the exact text provided in Reference Facts for Patient Name, Age, Gender, Hospital, and Test Results.\n"
                "2. ABSOLUTE ZERO-HALLUCINATION DIRECTIVE: DO NOT invent, assume, or fabricate ANY patient name (e.g. NEVER output fake names like 'Kunal Kumar'), fake dates, or fake disease statuses.\n"
                "3. Read the text line by line. Extract Patient Name (e.g. Mrs. SANTOSH DEVI), Age/Gender, Hospital Name, and Test Results (e.g. NON REACTIVE / POSITIVE) directly from Reference Facts.\n"
                "4. If a specific field (like Patient Name or DOB) is NOT explicitly present in Reference Facts, state clearly: 'Document mein yeh jankari nahi di gayi hai.'\n"
                "5. Always use structured markdown with emoji headings: `### 📋 Patient Details`, `### 🔬 Test Results & Values`, `### 💡 Key Summary`.\n\n"
            )
        else:
            doc_directive = ""


        # ── 4. Formatting rules
        formatting = (
            "MANDATORY FORMATTING RULES:\n"
            "- Always use neat Markdown with emoji headings (`### 📌 Overview`, `### 📋 Key Details`, `### 💡 Recommendations`).\n"
            "- Always start with a friendly 1-2 sentence overview with an emoji (e.g. 📌).\n"
            "- Use **bold text** for all test names, numerical values, medicine names, or important terms.\n"
            "- Use bullet points (`- `) with relevant emojis (e.g. ✅, ⚠️, 💊, ℹ️) for every list item.\n"
            "- Keep the answer well-spaced, concise, visually appealing, and super easy to read.\n"
        )

        # ── 5. Context block
        if chunks:
            context_block = "Reference Facts (from document / knowledge base):\n"
            for idx, c in enumerate(chunks, 1):
                context_block += f"Fact [{idx}]: {c['text']}\n\n"
        else:
            context_block = (
                "Reference Facts: No specific document/KB match found for this question.\n"
                "INSTRUCTION: Answer the user's question directly and concisely using your internal knowledge.\n\n"
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
