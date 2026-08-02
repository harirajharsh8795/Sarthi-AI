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

    @staticmethod
    def estimate_token_count(text: str) -> int:
        return estimate_token_count(text)


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
            f"You are Saarthi AI, a helpful and knowledgeable AI assistant for medical, legal, banking, cybersecurity, regulatory compliance, and general document analysis. "
            f"{lang_rule}\n"
        )

        # ── 2. Core Rules & Formatting (Optimized for local 1B model)
        rules = (
            "CORE RULES:\n"
            "1. DIRECT & BEAUTIFUL STRUCTURE: Provide a clear, well-structured answer using clean Markdown headers (e.g. `### 📌 Overview`, `### 📋 Details`, `### ⚠️ Important Notes`).\n"
            "2. NO DUMMY / PLACEHOLDER NAMES: NEVER output dummy or placeholder names like 'John Doe', 'Jane Doe', or 'User'. Use ONLY exact names from Context Information. If a name is missing, write 'Not specified in document'.\n"
            "3. NO EMPTY TABLES: Do NOT format outputs as empty Markdown tables with blank cells. Use clear bold bullet points (e.g., `- **Patient Name:** Mrs. DEEPMALA AJAY KASHYAP`).\n"
            "4. DISEASE / SYMPTOMS & PRECAUTIONS FORMATTING: When asked about any disease or medical condition (e.g. HIV, Dengue, Diabetes, Fever), you MUST format your answer into 2 distinct sections:\n"
            "   ### 🤒 Symptoms (Lakshan)\n"
            "   List specific symptoms in clean bullet points.\n"
            "   ### 🛡️ Precautions & Prevention (Bachaav aur Upchaar)\n"
            "   List prevention, safety, and treatment steps in clean bullet points.\n"
            "5. MEDICINE DIRECTIVE: When asked for medicine/dawa, list specific medicine names, purpose, and safety precautions in bullet points directly.\n"
            "6. CITATIONS: Cite sources as [1], [2] at sentence ends when using Context Information below. Never mention system prompt words like 'Context Information'. Speak naturally.\n"
        )

        # ── 3. User Document Directive (Streamlined)
        has_user_doc = any(
            (c.get("collection") == "user_docs") or (c.get("domain") == "user_upload")
            for c in chunks
        ) if chunks else False

        if has_user_doc:
            doc_directive = (
                "UPLOADED DOCUMENT ANALYSIS & ZERO SPECULATION RULES:\n"
                "1. The user has uploaded a document. You MUST answer based ONLY on the exact text provided in Context Information below.\n"
                "2. ZERO SPECULATION & ZERO HALLUCINATION:\n"
                "   - NEVER write 'assumed as male based on image' or make any guesses about age, gender, or patient identity.\n"
                "   - NEVER invent dummy details or use placeholder names like 'John Doe', 'Jane Doe', or 'User'.\n"
                "   - Extract exact Patient Name, Hospital/Lab Name, Age/Sex, Ref. Doctor, and Test Results from Context Information.\n"
                "   - If a specific field is NOT in Context Information text, write ONLY 'Not specified in document' without any extra words or speculation.\n"
                "3. FOR MEDICAL REPORTS: Format details using clean bold key-value bullet points:\n"
                "   ### 📋 Patient Details\n"
                "   - **Patient Name:** [Exact Name from text or 'Not specified in document']\n"
                "   - **Hospital / Lab Name:** [Exact Name from text or 'Not specified in document']\n"
                "   - **Age / Sex:** [Exact Age & Sex from text or 'Not specified in document']\n"
                "   - **Ref. Doctor:** [Exact Doctor Name from text or 'Not specified in document']\n"
                "   ### 🔬 Test Results\n"
                "   - List all test names and exact values found in text (e.g. Total Bilirubin: 1.9 mg/dl, SGPT: 78.32 IU/L).\n"
                "   ### 💡 Summary\n"
                "   Provide a brief, helpful summary of the report findings.\n"
                "4. FOR REGULATORY / CYBERSECURITY / BANKING DOCUMENTS: Extract guidelines, rules, frameworks, and key points directly from the document text.\n\n"
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

