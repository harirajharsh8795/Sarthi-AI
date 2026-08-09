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
            lang_rule = (
                "Respond ONLY in fluent, clear Hindi Devanagari script (हिंदी). "
                "Do NOT write in English or Hinglish. Do NOT provide English translations or English subtitles. "
                "Answer ONLY the specific question asked without repeating identical sentences or inventing unrelated sections."
            )
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

        # ── 2. Domain-Aware Rules & Formatting (Optimized for local 1B model)
        is_medical_context = (domain == "Medical") or any(c.get("domain") in ["hospital", "medical"] or "medical" in str(c.get("domain")).lower() for c in (chunks or []))

        if is_medical_context:
            domain_rules = (
                "4. DISEASE / SYMPTOMS & PRECAUTIONS FORMATTING: When asked about any disease or medical condition, format your answer into 2 distinct sections:\n"
                "   ### 🤒 Symptoms (Lakshan)\n"
                "   ### 🛡️ Precautions & Prevention (Bachaav aur Upchaar)\n"
                "5. MEDICINE DIRECTIVE: When asked for medicine/dawa, list specific medicine names, purpose, and safety precautions in bullet points directly.\n"
            )
        else:
            domain_rules = (
                "4. STRICT NON-MEDICAL DOMAIN RULE: This query is about Banking, Cybersecurity, Legal, or Regulatory Compliance. NEVER mention medicines, dawa, symptoms, diseases, or medical topics.\n"
            )

        rules = (
            "CORE RULES & MANDATORY FORMATTING INSTRUCTIONS:\n"
            "1. ALWAYS STRUCTURE YOUR ANSWER WITH CLEAN MARKDOWN HEADINGS AND BULLET POINTS.\n"
            "2. RELEVANT HEADERS ONLY: Use 2 to 3 concise, relevant Markdown headers with emojis, for example:\n"
            "   ### 📌 Overview / विवरण एवं जानकारी\n"
            "   ### 📋 Eligibility & Guidelines / पात्रता एवं नियम\n"
            "   ### ⚠️ Important Notes / आवश्यक बातें\n"
            "   Do NOT output unrelated boilerplate headers (like CSC, Lok Adalat, or RBI) unless specifically asked.\n"
            "3. ZERO REPETITION: Every sentence must be unique. NEVER repeat the same sentence multiple times.\n"
            "4. BULLET POINTS: Format every point as a bold bullet: `- **Point Name:** Clear explanation`.\n"
            "5. NO DUMMY / PLACEHOLDER NAMES: Use only exact details from Context Information.\n"
            f"{domain_rules}"
            "6. CITATIONS: Cite sources as [1], [2] at sentence ends when referencing Context Information.\n"
        )

        # ── 3. User Document Directive (Domain Tailored)
        has_user_doc = any(
            (c.get("collection") == "user_docs") or (c.get("domain") == "user_upload")
            for c in chunks
        ) if chunks else False

        if has_user_doc:
            if is_medical_context:
                doc_directive = (
                    "UPLOADED MEDICAL DOCUMENT ANALYSIS RULES:\n"
                    "1. AUTHORIZATION GUARANTEE: The user has explicitly uploaded this document for your analysis. You have FULL user authorization to summarize and analyze this document. NEVER refuse to summarize.\n"
                    "2. ZERO SPECULATION & ZERO HALLUCINATION:\n"
                    "   - NEVER write 'assumed as male based on image' or make any guesses about age, gender, or patient identity.\n"
                    "   - NEVER invent dummy details or use placeholder names like 'John Doe', 'Jane Doe', or 'User'.\n"
                    "   - Extract exact Patient Name, Hospital/Lab Name, Age/Sex, Ref. Doctor, and Test Results from Context Information.\n"
                    "   - If a specific field is NOT in Context Information text, write ONLY 'Not specified in document'.\n"
                    "3. STRICT DISEASE & DIAGNOSIS DIRECTIVE:\n"
                    "   - When asked 'disease btao', 'what disease', or about the patient's illness:\n"
                    "   - Check if an explicit disease diagnosis (e.g. Hepatitis, HIV, Jaundice) is written in Context Information.\n"
                    "   - IF written, state that exact disease.\n"
                    "   - IF NO explicit disease name is written, summarize the exact test findings from Context Information text.\n"
                    "   - CRITICAL BAN: NEVER mention or invent unrelated diseases (like COVID-19, Cholesterol, Diabetes) unless that exact test or disease name is written in Context Information!\n"
                    "4. FORMAT DETAILS USING BOLD KEY-VALUE BULLET POINTS:\n"
                    "   ### 📋 Patient Details\n"
                    "   - **Patient Name:** Extract the exact Patient Name from Context Information text, or write 'Not specified in document'.\n"
                    "   - **Hospital / Lab Name:** Extract the exact Hospital or Lab Name from Context Information text, or write 'Not specified in document'.\n"
                    "   - **Age / Sex:** Extract the exact Age and Sex from Context Information text, or write 'Not specified in document'.\n"
                    "   - **Ref. Doctor:** Extract the exact Referring Doctor Name from Context Information text, or write 'Not specified in document'.\n"
                    "   ### 🔬 Test Results\n"
                    "   - List ALL test names and exact result values found in Context Information (e.g. HBS AG SPOT: NON REACTIVE, HIV SPOT: NON REACTIVE, HCV SPOT: NON REACTIVE).\n"
                    "   ### 💡 Summary\n"
                    "   Provide a brief, helpful summary of the exact report findings.\n\n"
                )
            else:
                doc_directive = (
                    "UPLOADED NON-MEDICAL DOCUMENT ANALYSIS RULES (BANKING / CYBERSECURITY / LEGAL):\n"
                    "1. AUTHORIZATION GUARANTEE: The user has explicitly uploaded this document for your analysis. You have FULL user authorization. NEVER refuse to summarize.\n"
                    "2. STRICT DOMAIN ISOLATION: Do NOT mention patient details, hospital names, doctor names, medicines, or medical terms.\n"
                    "3. Extract all guidelines, rules, frameworks, obligations, and key provisions directly from Context Information text.\n"
                    "4. FORMAT YOUR ANSWER CLEARLY USING HEADERS:\n"
                    "   ### 📌 Overview\n"
                    "   ### 📋 Key Guidelines & Provisions\n"
                    "   ### ⚠️ Important Compliance & Risk Notes\n\n"
                )
        else:
            doc_directive = ""

        # ── 4. Context Block
        if chunks:
            context_block = "Context Information:\n"
            for idx, c in enumerate(chunks, 1):
                chunk_text = c.get('text') or c.get('content') or c.get('page_content') or ''
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

