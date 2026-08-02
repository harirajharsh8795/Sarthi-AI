"""
Saarthi AI — RAG Regression Test Suite
=======================================
Validates end-to-end retrieval quality across all three domains (Medical, Legal, Banking)
plus PDF-upload document queries. Catches cross-domain contamination and retrieval
priority regressions before they reach production.

Usage:
    # Run all regression tests (retrieval-only, no Ollama required)
    pytest backend/tests/test_regression_qa.py -v

    # Run only medical domain tests
    pytest backend/tests/test_regression_qa.py -v -k "medical"

    # Run only cross-domain contamination checks
    pytest backend/tests/test_regression_qa.py -v -k "contamination"

    # Run only PDF-upload tests (requires a running backend with seeded ChromaDB)
    pytest backend/tests/test_regression_qa.py -v -k "pdf_upload"
"""

import pytest
import sys
import os
import time
import uuid
import logging

# ---------------------------------------------------------------------------
# Path setup — ensure backend modules are importable
# ---------------------------------------------------------------------------
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BACKEND_DIR)

from intent_service import intent_service
from retrieval_router import (
    retrieve_context,
    normalize_hinglish_query,
    is_document_about_query,
)

logger = logging.getLogger("saarthi.regression_tests")

# ---------------------------------------------------------------------------
# Test configuration
# ---------------------------------------------------------------------------
# Session ID used for KB-only queries (no user docs attached)
KB_TEST_SESSION_ID = None  # None = skip user_docs retrieval entirely

# Domains considered "forbidden" per domain (truly non-overlapping concepts)
MEDICAL_FORBIDDEN = {"kyc", "loan", "emi", "cibil", "foreclosure", "home loan", "savings account"}
LEGAL_FORBIDDEN = {"paracetamol", "dosage", "antacid", "amoxicillin"}
BANKING_FORBIDDEN = {"appendicitis", "peritonitis", "paracetamol", "dosage", "antacid", "amoxicillin"}





# ═══════════════════════════════════════════════════════════════════════════
# DOMAIN TEST CASE DEFINITIONS
# Each case: (query, expected_domain, required_keywords_in_chunks, forbidden_keywords)
# ═══════════════════════════════════════════════════════════════════════════

MEDICAL_TEST_CASES = [
    # --- English ---
    (
        "What are the symptoms of dengue fever?",
        "Medical",
        ["dengue", "fever"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "How is diabetes diagnosed and what are normal blood sugar levels?",
        "Medical",
        ["diabetes", "blood sugar"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "What is the treatment for typhoid fever?",
        "Medical",
        ["typhoid"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "What medicines are used for chest pain?",
        "Medical",
        ["chest", "pain"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "What are the causes of kidney stone?",
        "Medical",
        ["kidney"],
        MEDICAL_FORBIDDEN,
    ),
    # --- Hinglish (Prompt 1 regression: pet dard should hit stomach_pain.md, NOT external PDFs) ---
    (
        "pet dard ki dva btao",
        "Medical",
        ["stomach", "pain"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "bukhar me kya karna chahiye",
        "Medical",
        ["fever"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "sir dard ki dawa batao",
        "Medical",
        ["headache"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "khansi ka ilaj kya hai",
        "Medical",
        ["cough"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "ulti rok ne ki dawa",
        "Medical",
        ["vomit"],
        MEDICAL_FORBIDDEN,
    ),
    # --- Hindi (Devanagari) ---
    (
        "मुझे बुखार है क्या करूं",
        "Medical",
        ["fever"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "पेट में जलन हो रही है",
        "Medical",
        ["stomach"],
        MEDICAL_FORBIDDEN,
    ),
    # --- Specific regression: .md file priority over ICMR PDFs ---
    (
        "stomach pain ka treatment btao",
        "Medical",
        ["stomach", "pain"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "liver ki bimari ke lakshan",
        "Medical",
        ["liver"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "cancer ke symptoms kya hain",
        "Medical",
        ["cancer"],
        MEDICAL_FORBIDDEN,
    ),
    (
        "heart attack ke warning signs",
        "Medical",
        ["heart"],
        MEDICAL_FORBIDDEN,
    ),
]

LEGAL_TEST_CASES = [
    # --- English ---
    (
        "How to file an FIR at the police station?",
        "Legal",
        ["fir"],
        LEGAL_FORBIDDEN,
    ),
    (
        "What are the rights of an arrested person?",
        "Legal",
        ["arrest", "right"],
        LEGAL_FORBIDDEN,
    ),
    (
        "How to file an RTI application?",
        "Legal",
        ["rti"],
        LEGAL_FORBIDDEN,
    ),
    (
        "What is the process for bail in India?",
        "Legal",
        ["bail"],
        LEGAL_FORBIDDEN,
    ),
    (
        "What is zero FIR and when can it be filed?",
        "Legal",
        ["zero", "fir"],
        LEGAL_FORBIDDEN,
    ),
    # --- Hinglish ---
    (
        "FIR kaise darj karein police station mein?",
        "Legal",
        ["fir"],
        LEGAL_FORBIDDEN,
    ),
    (
        "arrest hone ke baad kya rights hain?",
        "Legal",
        ["arrest", "right"],
        LEGAL_FORBIDDEN,
    ),
    (
        "consumer court mein complaint kaise karein?",
        "Legal",
        ["consumer", "complaint"],
        LEGAL_FORBIDDEN,
    ),
    (
        "anticipatory bail kya hoti hai?",
        "Legal",
        ["anticipatory", "bail"],
        LEGAL_FORBIDDEN,
    ),
    (
        "police notice aaye toh kya karein?",
        "Legal",
        ["police", "notice"],
        LEGAL_FORBIDDEN,
    ),
    # --- Hindi ---
    (
        "एफआईआर दर्ज करने की प्रक्रिया क्या है?",
        "Legal",
        ["fir"],
        LEGAL_FORBIDDEN,
    ),
    (
        "गिरफ्तारी के बाद क्या अधिकार हैं?",
        "Legal",
        ["arrest"],
        LEGAL_FORBIDDEN,
    ),
    # --- Specific topics ---
    (
        "What is BNSS Section 173?",
        "Legal",
        ["bnss"],
        LEGAL_FORBIDDEN,
    ),
    (
        "property dispute mein kya karna chahiye",
        "Legal",
        ["property"],
        LEGAL_FORBIDDEN,
    ),
    (
        "traffic challan ka process kya hai",
        "Legal",
        ["traffic"],
        LEGAL_FORBIDDEN,
    ),
    (
        "divorce ka process India mein",
        "Legal",
        ["divorce"],
        LEGAL_FORBIDDEN,
    ),
]

BANKING_TEST_CASES = [
    # --- English ---
    (
        "What documents are needed for KYC?",
        "Banking",
        ["kyc"],
        BANKING_FORBIDDEN,
    ),
    (
        "How to open a savings account in a bank?",
        "Banking",
        ["savings", "account"],
        BANKING_FORBIDDEN,
    ),
    (
        "What is the process for home loan application?",
        "Banking",
        ["home", "loan"],
        BANKING_FORBIDDEN,
    ),
    (
        "How to check CIBIL score?",
        "Banking",
        ["cibil"],
        BANKING_FORBIDDEN,
    ),
    (
        "What is loan foreclosure and prepayment?",
        "Banking",
        ["foreclosure"],
        BANKING_FORBIDDEN,
    ),
    # --- Hinglish ---
    (
        "bank me KYC kaise update karein?",
        "Banking",
        ["kyc"],
        BANKING_FORBIDDEN,
    ),
    (
        "home loan ke liye kya documents chahiye?",
        "Banking",
        ["home", "loan"],
        BANKING_FORBIDDEN,
    ),
    (
        "personal loan ka interest rate kitna hai?",
        "Banking",
        ["personal", "loan"],
        BANKING_FORBIDDEN,
    ),
    (
        "credit card se EMI kaise banaye?",
        "Banking",
        ["credit", "card"],
        BANKING_FORBIDDEN,
    ),

    (
        "mudra loan kya hai aur kaise milta hai?",
        "Banking",
        ["mudra", "loan"],
        BANKING_FORBIDDEN,
    ),
    # --- Hindi ---
    (
        "बैंक खाता कैसे खोलें?",
        "Banking",
        ["account"],
        BANKING_FORBIDDEN,
    ),
    (
        "लोन चुकाने में देरी हो तो क्या होता है?",
        "Banking",
        ["loan"],
        BANKING_FORBIDDEN,
    ),
    # --- Specific topics ---
    (
        "NRI account types in Indian banks",
        "Banking",
        ["nri", "account"],
        BANKING_FORBIDDEN,
    ),
    (
        "education loan process kya hai?",
        "Banking",
        ["education", "loan"],
        BANKING_FORBIDDEN,
    ),
    (
        "gold loan kaise milta hai?",
        "Banking",
        ["gold", "loan"],
        BANKING_FORBIDDEN,
    ),
    (
        "zero balance account kaise kholein?",
        "Banking",
        ["zero", "balance"],
        BANKING_FORBIDDEN,
    ),
]


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def _get_chunk_text_combined(chunks: list) -> str:
    """Concatenate all chunk texts into a single lowercase string for keyword search."""
    return " ".join(c.get("text", "") for c in chunks).lower()


def _get_chunk_sources(chunks: list) -> list:
    """Extract all source filenames from chunks."""
    return [c.get("source", "").lower() for c in chunks]


def _has_any_md_source(chunks: list) -> bool:
    """Check if any chunk originates from a curated .md file."""
    return any(
        s.endswith(".md") or s.endswith(".txt")
        for s in _get_chunk_sources(chunks)
    )


def _check_no_forbidden_keywords(combined_text: str, forbidden: set) -> list:
    """Returns list of forbidden keywords found in the combined text using exact word boundary matching."""
    import re
    found = []
    for kw in forbidden:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, combined_text, re.IGNORECASE):
            found.append(kw)
    return found



# ═══════════════════════════════════════════════════════════════════════════
# 1. INTENT CLASSIFICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestIntentClassification:
    """Verifies that the intent_service correctly classifies domain for all test queries."""

    @pytest.mark.parametrize(
        "query, expected_domain, _req_kw, _forbidden",
        MEDICAL_TEST_CASES,
        ids=[f"med_{i}" for i in range(len(MEDICAL_TEST_CASES))],
    )
    def test_medical_intent(self, query, expected_domain, _req_kw, _forbidden):
        result = intent_service.classify_query(query)
        assert result["domain"] == expected_domain, (
            f"Query '{query}' classified as '{result['domain']}', expected '{expected_domain}'"
        )

    @pytest.mark.parametrize(
        "query, expected_domain, _req_kw, _forbidden",
        LEGAL_TEST_CASES,
        ids=[f"legal_{i}" for i in range(len(LEGAL_TEST_CASES))],
    )
    def test_legal_intent(self, query, expected_domain, _req_kw, _forbidden):
        result = intent_service.classify_query(query)
        assert result["domain"] == expected_domain, (
            f"Query '{query}' classified as '{result['domain']}', expected '{expected_domain}'"
        )

    @pytest.mark.parametrize(
        "query, expected_domain, _req_kw, _forbidden",
        BANKING_TEST_CASES,
        ids=[f"bank_{i}" for i in range(len(BANKING_TEST_CASES))],
    )
    def test_banking_intent(self, query, expected_domain, _req_kw, _forbidden):
        result = intent_service.classify_query(query)
        assert result["domain"] == expected_domain, (
            f"Query '{query}' classified as '{result['domain']}', expected '{expected_domain}'"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 2. RETRIEVAL CORRECTNESS TESTS — KB-ONLY (no user docs)
# ═══════════════════════════════════════════════════════════════════════════

class TestRetrievalCorrectness:
    """
    Calls retrieve_context() with session_id=None (KB-only mode) and verifies:
      (a) At least one chunk is returned
      (b) Required keywords appear in the retrieved chunks
      (c) Chunks originate from curated .md files (not external PDFs)
    """

    @pytest.mark.parametrize(
        "query, expected_domain, required_keywords, _forbidden",
        MEDICAL_TEST_CASES,
        ids=[f"retrieval_med_{i}" for i in range(len(MEDICAL_TEST_CASES))],
    )
    def test_medical_retrieval(self, query, expected_domain, required_keywords, _forbidden):
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, f"No chunks retrieved for medical query: '{query}'"

        combined = _get_chunk_text_combined(chunks)
        for kw in required_keywords:
            assert kw.lower() in combined, (
                f"Required keyword '{kw}' not found in retrieved chunks for query: '{query}'"
            )

    @pytest.mark.parametrize(
        "query, expected_domain, required_keywords, _forbidden",
        LEGAL_TEST_CASES,
        ids=[f"retrieval_legal_{i}" for i in range(len(LEGAL_TEST_CASES))],
    )
    def test_legal_retrieval(self, query, expected_domain, required_keywords, _forbidden):
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, f"No chunks retrieved for legal query: '{query}'"

        combined = _get_chunk_text_combined(chunks)
        for kw in required_keywords:
            assert kw.lower() in combined, (
                f"Required keyword '{kw}' not found in retrieved chunks for query: '{query}'"
            )

    @pytest.mark.parametrize(
        "query, expected_domain, required_keywords, _forbidden",
        BANKING_TEST_CASES,
        ids=[f"retrieval_bank_{i}" for i in range(len(BANKING_TEST_CASES))],
    )
    def test_banking_retrieval(self, query, expected_domain, required_keywords, _forbidden):
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, f"No chunks retrieved for banking query: '{query}'"

        combined = _get_chunk_text_combined(chunks)
        for kw in required_keywords:
            assert kw.lower() in combined, (
                f"Required keyword '{kw}' not found in retrieved chunks for query: '{query}'"
            )


# ═══════════════════════════════════════════════════════════════════════════
# 3. .MD FILE PRIORITY TESTS — Prompt 1 regression guard
# ═══════════════════════════════════════════════════════════════════════════

class TestMdFilePriority:
    """
    Verifies that curated .md files from knowledge_base/ have absolute priority
    over external PDF files (e.g. icmr_treatment_guidelines_2019.pdf).

    This directly guards against the Prompt 1 bug where 'pet dard ki dva btao'
    returned citations from ICMR PDFs instead of stomach_pain.md.
    """

    MD_PRIORITY_CASES = [
        ("pet dard ki dva btao", ["stomach_pain.md", "stomach.md"]),
        ("bukhar me kya karna chahiye", ["fever.md"]),
        ("sir dard ki dawa batao", ["headache.md"]),
        ("khansi ka ilaj", ["cough.md"]),
        ("liver ki bimari", ["liver"]),
        ("home loan ke liye documents", ["home_loan.md"]),
        ("KYC process kya hai", ["kyc.md"]),
        ("FIR kaise darj karein", ["fir.md"]),
    ]

    @pytest.mark.parametrize(
        "query, expected_source_substrings",
        MD_PRIORITY_CASES,
        ids=[f"md_priority_{i}" for i in range(len(MD_PRIORITY_CASES))],
    )
    def test_md_sources_prioritized(self, query, expected_source_substrings):
        """Top retrieved chunks should come from local .md files, not external PDFs."""
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, f"No chunks retrieved for: '{query}'"

        # At least the top chunk should be from a .md file
        sources = _get_chunk_sources(chunks)
        top_source = sources[0] if sources else ""
        assert _has_any_md_source(chunks), (
            f"No .md source found in top chunks for '{query}'. "
            f"Sources returned: {sources}"
        )

        # Verify expected source file appears somewhere in top results
        any_match = any(
            any(substr.lower() in src for src in sources[:4])
            for substr in expected_source_substrings
        )
        assert any_match, (
            f"Expected sources {expected_source_substrings} not found in top 4 chunks. "
            f"Got: {sources[:4]}"
        )

    def test_no_icmr_pdf_for_pet_dard(self):
        """
        Regression test: 'pet dard ki dva btao' must NOT return icmr_treatment_guidelines PDF.
        This was the exact bug reported in Prompt 1.
        """
        result = retrieve_context("pet dard ki dva btao", session_id=None)
        chunks = result.get("context_chunks", [])
        sources = _get_chunk_sources(chunks)

        icmr_sources = [s for s in sources if "icmr" in s]
        assert len(icmr_sources) == 0, (
            f"ICMR PDF leaked into 'pet dard' results! Sources: {icmr_sources}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 4. CROSS-DOMAIN CONTAMINATION TESTS — Prompt 2 regression guard
# ═══════════════════════════════════════════════════════════════════════════

class TestCrossDomainContamination:
    """
    Ensures medical queries never return banking/legal chunks, legal queries
    never return medical/banking chunks, and banking queries never return
    medical/legal chunks. Catches the bug where unrelated PDF citations
    contaminated answers across domains.
    """

    @pytest.mark.parametrize(
        "query, _domain, _req_kw, forbidden_keywords",
        MEDICAL_TEST_CASES,
        ids=[f"contam_med_{i}" for i in range(len(MEDICAL_TEST_CASES))],
    )
    def test_medical_no_contamination(self, query, _domain, _req_kw, forbidden_keywords):
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        if not chunks:
            pytest.skip("No chunks retrieved — cannot test contamination")

        combined = _get_chunk_text_combined(chunks)
        found_forbidden = _check_no_forbidden_keywords(combined, forbidden_keywords)
        assert len(found_forbidden) == 0, (
            f"Cross-domain contamination in medical query '{query}': "
            f"found forbidden keywords {found_forbidden}"
        )

    @pytest.mark.parametrize(
        "query, _domain, _req_kw, forbidden_keywords",
        LEGAL_TEST_CASES,
        ids=[f"contam_legal_{i}" for i in range(len(LEGAL_TEST_CASES))],
    )
    def test_legal_no_contamination(self, query, _domain, _req_kw, forbidden_keywords):
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        if not chunks:
            pytest.skip("No chunks retrieved — cannot test contamination")

        combined = _get_chunk_text_combined(chunks)
        found_forbidden = _check_no_forbidden_keywords(combined, forbidden_keywords)
        assert len(found_forbidden) == 0, (
            f"Cross-domain contamination in legal query '{query}': "
            f"found forbidden keywords {found_forbidden}"
        )

    @pytest.mark.parametrize(
        "query, _domain, _req_kw, forbidden_keywords",
        BANKING_TEST_CASES,
        ids=[f"contam_bank_{i}" for i in range(len(BANKING_TEST_CASES))],
    )
    def test_banking_no_contamination(self, query, _domain, _req_kw, forbidden_keywords):
        result = retrieve_context(query, session_id=None)
        chunks = result.get("context_chunks", [])
        if not chunks:
            pytest.skip("No chunks retrieved — cannot test contamination")

        combined = _get_chunk_text_combined(chunks)
        found_forbidden = _check_no_forbidden_keywords(combined, forbidden_keywords)
        assert len(found_forbidden) == 0, (
            f"Cross-domain contamination in banking query '{query}': "
            f"found forbidden keywords {found_forbidden}"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 5. HINGLISH NORMALIZATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestHinglishNormalization:
    """Verifies that Hinglish medical terms are correctly expanded for retrieval."""

    NORMALIZATION_CASES = [
        ("pet dard ki dawa", ["stomach pain", "abdominal pain"]),
        ("bukhar hai", ["fever", "temperature"]),
        ("sir dard ho rha hai", ["headache", "migraine"]),
        ("khansi ka ilaj", ["cough", "treatment"]),
        ("seena dard ho raha", ["chest pain", "cardiac"]),
        ("ulti aa rhi hai", ["vomiting", "nausea"]),
        ("dawai chahiye", ["medicine", "medication"]),
    ]

    @pytest.mark.parametrize(
        "query, expected_expansions",
        NORMALIZATION_CASES,
        ids=[f"hinglish_{i}" for i in range(len(NORMALIZATION_CASES))],
    )
    def test_hinglish_expansion(self, query, expected_expansions):
        expanded = normalize_hinglish_query(query)
        for exp in expected_expansions:
            assert exp in expanded.lower(), (
                f"Expected '{exp}' in expanded query. Got: '{expanded}'"
            )


# ═══════════════════════════════════════════════════════════════════════════
# 6. DOCUMENT-ABOUT-QUERY TRIGGER TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestDocumentTriggerDetection:
    """Verifies document summary/brief trigger detection for uploaded documents."""

    POSITIVE_TRIGGERS = [
        "is pdf ka summary btao",
        "report explain kro",
        "mera document samjhao",
        "this file me kya hai",
        "summarize the uploaded file",
        "give me summary of my report",
        "explain my report",
        "is report me patient ka naam kya hai",
    ]

    NEGATIVE_TRIGGERS = [
        "pet dard ki dva btao",
        "KYC rule kya hai",
        "How to file FIR?",
        "home loan interest rate",
        "bukhar ka ilaj",
    ]

    @pytest.mark.parametrize("query", POSITIVE_TRIGGERS)
    def test_should_trigger_doc_retrieval(self, query):
        assert is_document_about_query(query) is True, (
            f"Query '{query}' should trigger document retrieval but didn't"
        )

    @pytest.mark.parametrize("query", NEGATIVE_TRIGGERS)
    def test_should_not_trigger_doc_retrieval(self, query):
        assert is_document_about_query(query) is False, (
            f"Query '{query}' should NOT trigger document retrieval but did"
        )


# ═══════════════════════════════════════════════════════════════════════════
# 7. PDF UPLOAD / DOCUMENT QUERY TESTS — Prompt 2 regression guard
# ═══════════════════════════════════════════════════════════════════════════

class TestPdfUploadQueries:
    """
    Tests that queries about uploaded documents correctly retrieve document chunks
    and do NOT contaminate results with unrelated KB content.

    These tests create a synthetic session with a test document ingested,
    then verify retrieval scoping. Requires ChromaDB to be accessible.

    NOTE: 5 of these cases specifically test content near the END of multi-page
    documents to catch the forced-retrieval bug from Prompt 1.
    """

    @pytest.fixture(scope="class")
    def test_session(self):
        """Create a test session and ingest a synthetic document for testing."""
        import session_manager
        import kb_pipeline

        session_id = f"regression_test_{uuid.uuid4().hex[:8]}"
        conv_id = f"conv_regression_{uuid.uuid4().hex[:8]}"

        # Create session and conversation in SQLite
        try:
            session_manager.get_or_create_session(session_id, display_name="Regression Test")
            session_manager.ensure_conversation_exists(conv_id, session_id)
        except Exception as ex:
            logger.warning(f"Could not create SQLite session: {ex}")

        # Create a multi-page synthetic test document
        test_doc_chunks = [
            # Page 1 — Patient header
            {
                "text": "Holy Family Hospital, New Delhi. Patient Name: Mrs. SANTOSH DEVI. "
                        "Age: 56 Years 7 Months 22 Days. Sex: Female. "
                        "Bill No: 1408299. Ward: Emergency.",
                "page_number": 1,
                "chunk_index": 0,
            },
            # Page 1 — Test results part 1
            {
                "text": "HBS AG SPOT TEST: NON REACTIVE. Sample Number: 1199768. "
                        "Date of Collection: 24/06/2025 at 11:25 AM.",
                "page_number": 1,
                "chunk_index": 1,
            },
            # Page 2 — Test results part 2
            {
                "text": "HIV SPOT TEST: NON REACTIVE. Method: Immunochromatography. "
                        "Reference Range: Non Reactive.",
                "page_number": 2,
                "chunk_index": 0,
            },
            # Page 3 — Test results part 3
            {
                "text": "HCV SPOT TEST: NON REACTIVE. Method: Rapid Immunochromatography. "
                        "Reference Range: Non Reactive. All serology markers negative.",
                "page_number": 3,
                "chunk_index": 0,
            },
            # Page 4 — Doctor signature and end notes
            {
                "text": "Verified by: Dr. Ramesh Kumar, MD Pathology. "
                        "Report authenticated. Digital signature applied. "
                        "Note: All results are within normal limits. "
                        "Patient advised routine follow-up after 6 months. "
                        "Hospital Contact: +91-11-26984222.",
                "page_number": 4,
                "chunk_index": 0,
            },
            # Page 5 — Billing and administrative (end of document)
            {
                "text": "Total Billing Amount: Rs. 2450. Payment Mode: Cash. "
                        "Receipt No: RC-2025-881234. UHID: HFH-2025-44591. "
                        "Insurance Claim: Not applicable. Discharge Summary attached.",
                "page_number": 5,
                "chunk_index": 0,
            },
        ]

        doc_id = f"doc_regression_{uuid.uuid4().hex[:8]}"

        # Ingest test chunks directly into ChromaDB
        try:
            collection = kb_pipeline.get_user_docs_collection()
            model = kb_pipeline.get_embedding_model()

            ids = []
            embeddings = []
            documents = []
            metadatas = []

            for chunk in test_doc_chunks:
                chunk_id = f"{doc_id}_p{chunk['page_number']}_c{chunk['chunk_index']}"
                emb = model.encode(chunk["text"]).tolist()

                ids.append(chunk_id)
                embeddings.append(emb)
                documents.append(chunk["text"])
                metadatas.append({
                    "session_id": session_id,
                    "conversation_id": conv_id,
                    "document_id": doc_id,
                    "original_filename": "medical_report_test.webp",
                    "filename": "medical_report_test.webp",
                    "domain_hint": "user_upload",
                    "domain": "user_upload",
                    "page_number": chunk["page_number"],
                    "chunk_index": chunk["chunk_index"],
                    "language": "en",
                    "vector_norm": float(sum(x**2 for x in emb) ** 0.5),
                })

            collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas,
            )

            # Also register document in SQLite
            try:
                session_manager.create_document_record(
                    document_id=doc_id,
                    session_id=session_id,
                    conversation_id=conv_id,
                    original_filename="medical_report_test.webp",
                    file_type="image/webp",
                    domain_hint="medical",
                    ocr_used=True,
                    page_count=5,
                    chunk_count=len(test_doc_chunks),
                    status="indexed",
                )
            except Exception as e:
                logger.warning(f"Could not register doc in SQLite: {e}")



        except Exception as e:
            pytest.skip(f"Could not set up test document in ChromaDB: {e}")

        yield {
            "session_id": session_id,
            "conversation_id": conv_id,
            "document_id": doc_id,
            "chunk_count": len(test_doc_chunks),
        }

        # Cleanup: remove test chunks from ChromaDB
        try:
            collection = kb_pipeline.get_user_docs_collection()
            collection.delete(where={"session_id": session_id})
        except Exception:
            pass

    # --- Page 1 tests (first-page content) ---
    def test_patient_name_retrieval(self, test_session):
        """Patient name (Mrs. SANTOSH DEVI) should be in retrieved chunks."""
        result = retrieve_context(
            "patient ka naam kya hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks retrieved for patient name query"
        combined = _get_chunk_text_combined(chunks)
        assert "santosh devi" in combined, (
            f"Patient name 'SANTOSH DEVI' not found in chunks. Got: {combined[:200]}"
        )

    def test_first_test_result_retrieval(self, test_session):
        """HBS AG test result should be retrievable."""
        result = retrieve_context(
            "HBS AG test ka result kya hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for HBS AG query"
        combined = _get_chunk_text_combined(chunks)
        assert "non reactive" in combined

    # --- Page 2-3 tests (middle pages) ---
    def test_hiv_test_retrieval(self, test_session):
        """HIV test result from page 2 should be retrievable."""
        result = retrieve_context(
            "HIV test ka result btao",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for HIV test query"
        combined = _get_chunk_text_combined(chunks)
        assert "hiv" in combined
        assert "non reactive" in combined

    def test_hcv_test_retrieval(self, test_session):
        """HCV test result from page 3 should be retrievable."""
        result = retrieve_context(
            "HCV test result kya hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for HCV test query"
        combined = _get_chunk_text_combined(chunks)
        assert "hcv" in combined

    # --- Page 4-5 tests (END of multi-page document — Prompt 1 regression) ---
    def test_doctor_name_retrieval_late_page(self, test_session):
        """Doctor name from page 4 should be retrievable (forced-retrieval end-of-doc test)."""
        result = retrieve_context(
            "report me doctor ka naam kya hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for doctor name query"
        combined = _get_chunk_text_combined(chunks)
        assert "ramesh kumar" in combined, (
            f"Doctor name from page 4 not found. Chunks: {combined[:200]}"
        )

    def test_follow_up_advice_late_page(self, test_session):
        """Follow-up advice from page 4 should appear in forced retrieval."""
        result = retrieve_context(
            "patient ko follow up kab karna hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for follow-up query"
        combined = _get_chunk_text_combined(chunks)
        assert "6 months" in combined or "follow-up" in combined, (
            f"Follow-up info from page 4 not found in chunks"
        )

    def test_billing_amount_last_page(self, test_session):
        """Billing amount from page 5 (last page) should be retrievable."""
        result = retrieve_context(
            "total bill kitna hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for billing query"
        combined = _get_chunk_text_combined(chunks)
        assert "2450" in combined, (
            f"Billing amount Rs. 2450 from last page not found. Chunks: {combined[:200]}"
        )

    def test_receipt_number_last_page(self, test_session):
        """Receipt number from page 5 (last page) should be retrievable."""
        result = retrieve_context(
            "receipt number kya hai report ka",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for receipt query"
        combined = _get_chunk_text_combined(chunks)
        assert "rc-2025-881234" in combined, (
            f"Receipt number from last page not found"
        )

    def test_hospital_contact_late_page(self, test_session):
        """Hospital contact from page 4 should be retrievable."""
        result = retrieve_context(
            "hospital ka contact number kya hai",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        assert len(chunks) > 0, "No chunks for hospital contact query"
        combined = _get_chunk_text_combined(chunks)
        assert "26984222" in combined, (
            f"Hospital contact from page 4 not found"
        )

    def test_no_kb_contamination_in_doc_query(self, test_session):
        """
        When a user asks about their uploaded report, the chunks should ONLY
        come from user_docs collection, NOT from knowledge_base.
        This guards against the cross-conversation doc leak bug.
        """
        result = retrieve_context(
            "give me summary of my report",
            test_session["session_id"],
            test_session["conversation_id"],
        )
        chunks = result.get("context_chunks", [])
        if not chunks:
            pytest.skip("No chunks retrieved")

        for chunk in chunks:
            assert chunk.get("collection") == "user_docs", (
                f"KB chunk leaked into document query! Source: {chunk.get('source')}, "
                f"Collection: {chunk.get('collection')}"
            )


# ═══════════════════════════════════════════════════════════════════════════
# 8. PROMPT BUILDER SANITY TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestPromptBuilderSanity:
    """Verifies prompt_builder produces grounded, non-hallucinating prompts."""

    def test_user_doc_prompt_has_zero_hallucination_rule(self):
        from prompt_builder import prompt_builder

        chunks = [
            {
                "text": "Patient Name: Mrs. SANTOSH DEVI. HIV: NON REACTIVE.",
                "collection": "user_docs",
                "domain": "user_upload",
                "index": 1,
            }
        ]
        prompt = prompt_builder.build_adaptive_prompt(
            query="give me summary of report",
            chunks=chunks,
            language="English",
            domain="Medical",
            intent="QA",
        )
        assert "ZERO-HALLUCINATION" in prompt or "STRICT FACTUAL" in prompt, (
            "Prompt for user document query missing zero-hallucination grounding rule"
        )
        assert "SANTOSH DEVI" in prompt, (
            "Patient name from chunk not present in constructed prompt"
        )

    def test_kb_prompt_does_not_leak_document_rules(self):
        from prompt_builder import prompt_builder

        chunks = [
            {
                "text": "Stomach pain treatment includes antacids and lifestyle changes.",
                "collection": "knowledge_base",
                "domain": "medical",
                "index": 1,
            }
        ]
        prompt = prompt_builder.build_adaptive_prompt(
            query="pet dard ki dawa",
            chunks=chunks,
            language="Hinglish",
            domain="Medical",
            intent="QA",
        )
        # KB queries should NOT have the document-specific hallucination guard
        assert "DOCUMENT REPORT" not in prompt, (
            "KB query prompt incorrectly includes DOCUMENT REPORT directive"
        )
        assert "Context Information" in prompt or "Reference Facts" in prompt


# ═══════════════════════════════════════════════════════════════════════════
# MAIN — Run with verbose output when executed directly
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-x"])
