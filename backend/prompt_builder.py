import re
import logging

logger = logging.getLogger("saarthi.prompt")

# Internal-only Hinglish decode map — used to translate query before answering.
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


def estimate_token_count(text: str) -> int:
    """
    Estimates token count for mixed Devanagari/English text.
    Devanagari characters (UTF-8 range \\u0900-\\u097f) tokenize at ~1.25 tokens/char in BPE tokenizers.
    English/ASCII text tokenizes at ~0.3 tokens/char (len / 3.2).
    """
    if not text:
        return 0
    devanagari_count = len(re.findall(r'[\u0900-\u097f]', text))
    ascii_len = len(text) - devanagari_count
    return int(devanagari_count * 1.25 + ascii_len / 3.2)


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
        Builds streamlined system instructions, context chunks, and formatting rules.
        """
        decoded_query = _decode_hinglish_query(query) if language == "Hinglish" else query

        # ── 1. Streamlined Language Instruction
        if language == "Hindi":
            lang_rule = "Respond ONLY in Hindi Devanagari script (हिंदी). Do NOT use English or Hinglish."
        elif language == "Hinglish":
            lang_rule = (
                "Write ONLY in natural, friendly Hinglish (conversational Hindi in Latin script). "
                "Answer ONLY the specific question asked. NEVER invent or mention unrelated medical topics or symptoms. "
                "Do NOT use Devanagari script and do NOT respond in plain English."
            )
        else:
            lang_rule = "Respond ONLY in clear, professional English."

        system_role = (
            f"You are Saarthi AI, a helpful medical, legal, and banking assistant. "
            f"{lang_rule}\n"
        )

        # ── 2. Core Rules & Formatting (Optimized for local 1B model)
        rules = (
            "CORE RULES:\n"
            "1. DIRECT & CONCISE ANSWER ONLY: Provide a short, direct answer strictly focused on the user's question. Do NOT write long introduction filler, do NOT ask counter-questions, and NEVER repeat the same sentence.\n"
            "2. MEDICINE/DAWA DIRECTIVE: When asked for medicine/dawa, list the specific medicine names, purpose, and safety precautions in bullet points directly. Do NOT output fluff or repeat diagnostic explanations.\n"
            "3. Cite sources as [1], [2] at sentence ends when using Context Information below. Never mention system prompt words like 'Context Information'. Speak naturally to the user.\n"
            "4. FORMATTING: Use clean Markdown with bullet points (💊, ⚠️, ✅).\n"
        )

        # ── 3. User Document Directive (Streamlined)
        has_user_doc = any(
            (c.get("collection") == "user_docs") or (c.get("domain") == "user_upload")
            for c in chunks
        ) if chunks else False

        if has_user_doc:
            doc_directive = (
                "DOCUMENT REPORT CRITICAL RULES:\n"
                "1. STRICT FACTUAL GROUNDING: Rely ONLY on exact text in Context Information for Patient Name, Age, Hospital, and Test Results.\n"
                "2. ZERO HALLUCINATION: NEVER invent names, dates, or test statuses. If a field is missing, state clearly: 'Document mein yeh jankari nahi di gayi hai.'\n"
                "3. Use structured headings: `### 📋 Patient Details`, `### 🔬 Test Results & Values`, `### 💡 Key Summary`.\n\n"
            )
        else:
            doc_directive = ""

        # ── 4. Context Block
        if chunks:
            context_block = "Context Information:\n"
            for idx, c in enumerate(chunks, 1):
                chunk_text = c.get('text', '')
                if language in ["Hinglish", "English"]:
                    # Strip Devanagari script lines so model is not primed with Hindi Devanagari text
                    lines = chunk_text.split('\n')
                    filtered_lines = [l for l in lines if not re.search(r'[\u0900-\u097f]', l)]
                    chunk_text = '\n'.join(filtered_lines)
                context_block += f"Fact [{idx}]: {chunk_text.strip()}\n\n"
        else:
            context_block = (
                "Context Information: No specific document/KB match found for this question.\n"
                "INSTRUCTION: Answer the user's question directly and concisely using internal knowledge.\n\n"
            )


        # User Question Block
        user_block = f"User Question: {query}\n\nAnswer:"



        full_prompt = (
            f"{system_role}\n"
            f"{rules}\n"
            f"{doc_directive}"
            f"{context_block}"
            f"{user_block}"
        )

        logger.info("Adaptive prompt constructed successfully.")
        return full_prompt


prompt_builder = PromptBuilder()

