import os
import time
import kb_pipeline
from logger_config import logger

# Seed sources as provided in user request
SEED_DOCUMENT_SOURCES = [
    {
        "domain": "constitution_and_general_law",
        "documents": [
            {
                "title": "Constitution of India (English, official, as amended)",
                "url": "https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2024/07/20240716890312078.pdf",
                "filename": "constitution_of_india_en.pdf",
                "language": "en"
            },
            {
                "title": "Constitution of India (Hindi, official, as amended)",
                "url": "https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2023/05/2023050186.pdf",
                "filename": "constitution_of_india_hi.pdf",
                "language": "hi"
            }
        ]
    },
    {
        "domain": "legal",
        "documents": [
            {
                "title": "Bharatiya Nyaya Sanhita 2023 (English, official IndiaCode) - replaces IPC",
                "url": "https://www.indiacode.nic.in/bitstream/123456789/20062/1/a202345.pdf",
                "filename": "bharatiya_nyaya_sanhita_2023_en.pdf",
                "language": "en"
            },
            {
                "title": "Bharatiya Nyaya Sanhita 2023 (Hindi, official IndiaCode)",
                "url": "https://www.indiacode.nic.in/bitstream/123456789/21069/1/bns__iiitmanipur_english+manipuri_compressed.pdf",
                "filename": "bharatiya_nyaya_sanhita_2023_hi.pdf",
                "language": "hi",
                "note": "Verify on download that this file actually contains the Hindi text; if the linked file turns out to be bilingual English+Manipuri instead, search indiacode.nic.in for the dedicated Hindi BNS PDF and substitute it.",
                "fallback_url": "https://mha.gov.in/sites/default/files/2024-06/BNS_Hindi_24062024.pdf"
            },
            {
                "title": "Consumer Protection Act 2019 (English, official IndiaCode)",
                "url": "http://ncdrc.nic.in/bare_acts/CPA2019.pdf",
                "filename": "consumer_protection_act_2019_en.pdf",
                "language": "en"
            },
            {
                "title": "Right to Information Act 2005 (English, official)",
                "url": "https://cic.gov.in/sites/default/files/RTI-Act_English.pdf",
                "filename": "rti_act_2005_en.pdf",
                "language": "en"
            },
            {
                "title": "Right to Information Act 2005 (Hindi, official)",
                "url": "https://www.indiacode.nic.in/bitstream/123456789/2065/2/H2005.pdf",
                "filename": "rti_act_2005_hi.pdf",
                "language": "hi"
            },
            {
                "title": "Bharatiya Nagarik Suraksha Sanhita 2023 (BNSS) - Full Act (replaces CrPC)",
                "url": "https://www.indiacode.nic.in/bitstream/123456789/20340/1/bnss,_2023.pdf",
                "filename": "bnss_2023_full.pdf",
                "language": "en"
            },
            {
                "title": "BNSS 2023 Handbook - FIR, Arrest, Bail Key Sections (BPRD)",
                "url": "https://bprd.nic.in/uploads/pdf/BNSS_Handbook_English.pdf",
                "filename": "bnss_2023_handbook.pdf",
                "language": "en"
            },
            {
                "title": "Legal Aid Services - National Legal Services Authority (NALSA) schemes",
                "url": "https://nalsa.gov.in/sites/default/files/schemes/scheme-for-legal-aid-clinics-2010.pdf",
                "filename": "nalsa_legal_aid_scheme.pdf",
                "language": "en"
            },
            {
                "title": "Motor Vehicles Act - Key sections on accidents, insurance claims",
                "url": "https://www.indiacode.nic.in/bitstream/123456789/2154/1/motor_vehicles_act_1988.pdf",
                "filename": "motor_vehicles_act_1988.pdf",
                "language": "en"
            }
        ]
    },
    {
        "domain": "banking",
        "documents": [
            {
                "title": "RBI Master Direction - KYC norms",
                "url": "https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/MD18KYCF6E92C82E1E1419D87323E3869BC9F13.pdf",
                "filename": "rbi_master_direction_kyc_en.pdf",
                "language": "en"
            },
            {
                "title": "RBI - Foreclosure charges and pre-payment penalty circular",
                "url": "https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/DBC070514DF.pdf",
                "filename": "rbi_foreclosure_charges_circular_en.pdf",
                "language": "en"
            },
            {
                "title": "RBI - Home Loans Foreclosure Charges Pre-payment Penalty (2012 circular)",
                "url": "https://www.rbi.org.in/commonman/Upload/English/Notification/PDFs/41YC01072013KF.pdf",
                "filename": "rbi_home_loan_foreclosure_2012_en.pdf",
                "language": "en"
            }
        ]
    },
    {
        "domain": "hospital",
        "documents": [
            {
                "title": "IRDAI Master Circular on Health Insurance Business 2024",
                "url": "https://irdai.gov.in/documents/37343/365525/%e0%a4%b8%e0%a5%8d%e0%a4%b5%e0%a4%be%e0%a4%b8%e0%a5%8d%e0%a4%a5%e0%a5%8d%e0%a4%af+%e0%a4%ac%e0%a5%80%e0%a4%ae%e0%a4%be+%e0%a4%b5%e0%a5%8d%e0%a4%af%e0%a4%b5%e0%a4%b8%e0%a4%be%e0%a4%af+%e0%a4%aa%e0%a4%b0+%e0%a4%ae%e0%a4%be%e0%a4%b8%e0%a5%8d%e0%a4%9f%e0%a4%b0+%e0%a4%aa%e0%a4%b0%e0%a4%bf%e0%a4%aa%e0%a4%a4%e0%a5%8d%e0%a4%b0+_+Master+Circular++on+Health++Insurance+Business++29052024.pdf/5e707a91-b5de-1ec1-cf18-b66273a6839d?t=1716962621002&version=1.0",
                "filename": "irdai_health_insurance_master_circular_2024_en.pdf",
                "language": "en",
                "note": "This is a dynamic IRDAI document portal URL. Verify it resolves to a PDF at download time.",
                "unstable": True
            },
            {
                "title": "NHM Standard Treatment Guidelines - Fever/Malaria (IMNCI)",
                "url": "https://nhm.gov.in/images/pdf/programmes/child-health/guidelines/imnci_chart_booklet.pdf",
                "filename": "nhm_fever_malaria_imnci_guidelines.pdf",
                "language": "en"
            },
            {
                "title": "NHM Standard Treatment Guidelines - Hypertension (Full)",
                "url": "https://nhm.gov.in/images/pdf/guidelines/nrhm-guidelines/stg/Hypertension_full.pdf",
                "filename": "nhm_stg_hypertension.pdf",
                "language": "en"
            },
            {
                "title": "NHM Standard Treatment Guidelines - Tuberculosis",
                "url": "https://www.nhm.gov.in/images/pdf/guidelines/nrhm-guidelines/stg/stg-tb.pdf",
                "filename": "nhm_stg_tuberculosis.pdf",
                "language": "en"
            },
            {
                "title": "NHM Standard Treatment Guidelines - Malaria",
                "url": "https://www.nhm.gov.in/images/pdf/guidelines/nrhm-guidelines/stg/malaria-stg.pdf",
                "filename": "nhm_stg_malaria.pdf",
                "language": "en"
            },
            {
                "title": "NHM Standard Treatment Guidelines - Dengue",
                "url": "https://www.nhm.gov.in/images/pdf/guidelines/nrhm-guidelines/stg/dengue.pdf",
                "filename": "nhm_stg_dengue.pdf",
                "language": "en"
            },
            {
                "title": "NHM Standard Treatment Guidelines - Enteric Fever (Typhoid)",
                "url": "https://nhm.gov.in/images/pdf/guidelines/nrhm-guidelines/stg/enteric-fever.pdf",
                "filename": "nhm_stg_typhoid.pdf",
                "language": "en"
            },
            {
                "title": "NHM Operational Guidelines - NCDs (Diabetes, Hypertension, Cancer, Stroke)",
                "url": "https://nhm.gov.in/images/pdf/NHM/NHM-Guidelines/Operational_Guidelines_NCDs.pdf",
                "filename": "nhm_operational_guidelines_ncds.pdf",
                "language": "en"
            },
            {
                "title": "NHM Medical Officers Training - NCD Risk Factors and Screening",
                "url": "https://nhm.gov.in/New-Update-2025-26/Whats-new/NCD-Medical-Officers.pdf",
                "filename": "nhm_ncd_medical_officers_training.pdf",
                "language": "en"
            },
            {
                "title": "ICMR Standard Treatment Guidelines 2019",
                "url": "https://main.icmr.nic.in/sites/default/files/guidelines/Treatment_Guidelines_2019_Final.pdf",
                "filename": "icmr_treatment_guidelines_2019.pdf",
                "language": "en"
            }
        ]
    }
]

def main():
    logger.debug("=== Saarthi AI Stage 0: Knowledge Base Seeding ===")
    
    # 1. Initialize folders and SQLite DB
    kb_pipeline.init_directories()
    kb_pipeline.init_db()
    
    # Flatten the document list for processing
    flat_docs = []
    for group in SEED_DOCUMENT_SOURCES:
        domain = group["domain"]
        for doc in group["documents"]:
            flat_docs.append((domain, doc))
            
    # Process each document
    for domain, doc in flat_docs:
        title = doc["title"]
        url = doc["url"]
        filename = doc["filename"]
        language = doc["language"]
        unstable = doc.get("unstable", False)
        
        save_dir = os.path.join(kb_pipeline.KB_DIR, domain, language)
        save_path = os.path.join(save_dir, filename)
        
        logger.debug(f"\n--- Processing: {title} ---")
        
        # Check SQLite db state
        existing_doc = kb_pipeline.get_document_by_url(url)
        
        # Check if file exists and is indexed
        if os.path.exists(save_path) and existing_doc and existing_doc["status"] == "indexed":
            logger.debug(f"Skipping download & index for {filename} (Already exists locally and indexed in SQLite).")
            kb_pipeline.upsert_document_record(
                domain=domain, language=language, filename=filename, source_url=url,
                discovered_via="seed_list", status="skipped_exists",
                page_count=existing_doc["page_count"], chunk_count=existing_doc["chunk_count"]
            )
            continue
            
        download_success = False
        
        # If the file already exists locally, we skip downloading but still index it if not indexed
        if os.path.exists(save_path):
            logger.debug(f"File {filename} already exists locally. Skipping download.")
            download_success = True
        else:
            # Download file
            download_success = kb_pipeline.download_file(url, save_path, unstable=unstable)
            
            if not download_success:
                logger.debug(f"Failed to download {filename} from {url}.")
                kb_pipeline.upsert_document_record(
                    domain=domain, language=language, filename=filename, source_url=url,
                    discovered_via="seed_list", status="failed"
                )
                continue
                
            # Verify BNS Hindi file content
            if filename == "bharatiya_nyaya_sanhita_2023_hi.pdf":
                logger.debug("Checking BNS Hindi PDF content validity...")
                try:
                    pages_text, detected_lang = kb_pipeline.extract_text_and_language(save_path, "hi")
                    
                    if detected_lang != "hi":
                        logger.debug(f"Warning: BNS Hindi PDF has detected language '{detected_lang}' instead of 'hi'.")
                        fallback_url = doc["fallback_url"]
                        logger.debug(f"Downloading dedicated Hindi BNS PDF from fallback URL: {fallback_url}")
                        fallback_success = kb_pipeline.download_file(fallback_url, save_path)
                        if fallback_success:
                            logger.debug("Successfully downloaded fallback BNS Hindi PDF.")
                        else:
                            logger.debug("Warning: Failed to download fallback BNS Hindi PDF. Keeping primary file.")
                except Exception as e:
                    logger.debug(f"Error validating BNS Hindi PDF: {e}")
            
            # Record download success in SQLite
            now_str = time.strftime("%Y-%m-%d %H:%M:%S")
            kb_pipeline.upsert_document_record(
                domain=domain, language=language, filename=filename, source_url=url,
                discovered_via="seed_list", status="downloaded", downloaded_at=now_str
            )
            
        # Index document if download succeeded
        if download_success:
            page_count, chunk_count, index_status = kb_pipeline.index_document(
                domain=domain, language=language, filename=filename, source_url=url,
                discovered_via="seed_list", file_path=save_path
            )
            logger.debug(f"Indexing finished: {index_status} (Pages: {page_count}, Chunks: {chunk_count})")

if __name__ == "__main__":
    main()
