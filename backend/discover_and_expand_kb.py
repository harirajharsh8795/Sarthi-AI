import os
import re
import time
import hashlib
import urllib.parse
import requests
from bs4 import BeautifulSoup
import kb_pipeline

# Configuration
MAX_AUTO_DOCS_PER_DOMAIN = 15  # Default cap of 15 documents per domain
ALLOWED_DOMAINS = [
    "rbi.org.in",
    "irdai.gov.in",
    "indiacode.nic.in",
    "rti.gov.in",
    "legislative.gov.in",
    "consumeraffairs.gov.in",
    "consumeraffairs.nic.in",
    "icmr.gov.in",
    "main.icmr.nic.in",
    "policyholder.gov.in",
    "ncdrc.nic.in",
    "cic.gov.in"
]

STARTING_PAGES = [
    {"domain": "banking", "url": "https://www.rbi.org.in/commonman/english/scripts/MasterCircular.aspx"},
    {"domain": "banking", "url": "https://www.rbi.org.in/commonman/english/scripts/FAQs.aspx"},
    {"domain": "legal", "url": "https://www.indiacode.nic.in/handle/123456789/1362/browse?type=actyear"},
    {"domain": "hospital", "url": "https://irdai.gov.in/health-dept"},
    {"domain": "hospital", "url": "https://policyholder.gov.in/how-to-make-a-claim-health"}
]

def is_allowed_domain(url):
    """Checks if the URL's hostname belongs to the allowed domains list."""
    try:
        parsed = urllib.parse.urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False
        hostname = hostname.lower()
        
        for domain in ALLOWED_DOMAINS:
            if hostname == domain or hostname.endswith("." + domain):
                return True
        return False
    except Exception:
        return False

def extract_pdf_links(page_url):
    """Fetches a page and extracts all possible PDF or document download links."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    links = set()
    try:
        print(f"Fetching page: {page_url}...")
        response = requests.get(page_url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"Failed to fetch starting page. Status: {response.status_code}")
            return links
            
        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            abs_url = urllib.parse.urljoin(page_url, href)
            
            # De-fragment URL
            abs_url = abs_url.split("#")[0]
            
            parsed = urllib.parse.urlparse(abs_url)
            path = parsed.path.lower()
            query = parsed.query.lower()
            
            is_candidate = False
            # Standard PDF file ending or PDF query parameter
            if path.endswith(".pdf") or "filetype=pdf" in query or "format=pdf" in query:
                is_candidate = True
            # Check for standard document portal paths
            elif any(kw in abs_url.lower() for kw in ["/bitstream/", "/documents/", "/download", "upload/english/notification", "/handle/"]):
                is_candidate = True
                
            if is_candidate:
                links.add(abs_url)
                
    except Exception as e:
        print(f"Error fetching/parsing {page_url}: {e}")
        
    return links

def main():
    print("=== Saarthi AI Stage 0: Auto-Discovery & KB Expansion ===")
    
    kb_pipeline.init_directories()
    kb_pipeline.init_db()
    
    # Track document counts for logging summary
    found_totals = {}
    downloaded_totals = {}
    
    for page_info in STARTING_PAGES:
        domain = page_info["domain"]
        start_url = page_info["url"]
        
        found_totals.setdefault(domain, 0)
        downloaded_totals.setdefault(domain, 0)
        
        print(f"\n--- Crawling Start Page for {domain}: {start_url} ---")
        discovered_links = extract_pdf_links(start_url)
        print(f"Discovered {len(discovered_links)} potential document links.")
        
        valid_links = []
        for link in discovered_links:
            # 1. Filter by allowed domains only
            if not is_allowed_domain(link):
                # Print non-verbose message to avoid log clutter
                continue
                
            # 2. De-duplicate against SQLite by source_url
            existing = kb_pipeline.get_document_by_url(link)
            if existing:
                # Document is already recorded (downloaded/indexed/failed)
                continue
                
            valid_links.append(link)
            
        found_totals[domain] += len(valid_links)
        print(f"Filtered to {len(valid_links)} new candidate links (after allowed-domains check and DB de-duplication).")
        
        # Process new links up to the cap
        download_count = 0
        for link in valid_links:
            # Check cap
            if downloaded_totals[domain] >= MAX_AUTO_DOCS_PER_DOMAIN:
                print(f"Reached MAX_AUTO_DOCS_PER_DOMAIN limit of {MAX_AUTO_DOCS_PER_DOMAIN} for domain '{domain}'. Skipping further candidates.")
                break
                
            print(f"\nProcessing candidate link: {link}")
            
            # Generate a temporary path to download and inspect language
            url_hash = hashlib.md5(link.encode("utf-8")).hexdigest()
            temp_filename = f"temp_{url_hash}.pdf"
            temp_path = os.path.join(kb_pipeline.KB_DIR, domain, temp_filename)
            
            success = kb_pipeline.download_file(link, temp_path)
            if not success:
                print(f"Failed to download candidate: {link}")
                kb_pipeline.upsert_document_record(
                    domain=domain, language="unknown", filename=temp_filename, source_url=link,
                    discovered_via="auto_crawl", status="failed"
                )
                continue
                
            # Extract language of PDF first page to see if it is en or hi
            try:
                pages_text, detected_lang = kb_pipeline.extract_text_and_language(temp_path, "unknown")
                
                if detected_lang not in ["hi", "en"]:
                    print(f"Skipping PDF {link} because detected language '{detected_lang}' is neither Hindi ('hi') nor English ('en').")
                    kb_pipeline.upsert_document_record(
                        domain=domain, language=detected_lang, filename=temp_filename, source_url=link,
                        discovered_via="auto_crawl", status="skipped_unsupported_language"
                    )
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    continue
                    
                # Safe clean filename
                parsed_url = urllib.parse.urlparse(link)
                base_name = os.path.basename(parsed_url.path)
                if not base_name or not base_name.lower().endswith(".pdf"):
                    base_name = f"auto_{url_hash}.pdf"
                else:
                    base_name = urllib.parse.unquote(base_name)
                    base_name = re.sub(r"[^\w\-_.]", "_", base_name)
                    if not base_name.endswith(".pdf"):
                        base_name += ".pdf"
                        
                # Prepend domain/crawled prefix to avoid collision
                clean_filename = f"crawled_{base_name}"
                
                # Route file to its final destination
                final_dir = os.path.join(kb_pipeline.KB_DIR, domain, detected_lang)
                final_path = os.path.join(final_dir, clean_filename)
                
                # Move from temp to final
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.rename(temp_path, final_path)
                print(f"Routed document to {final_path} (Detected Lang: {detected_lang})")
                
                # Insert row to SQLite as downloaded
                now_str = time.strftime("%Y-%m-%d %H:%M:%S")
                kb_pipeline.upsert_document_record(
                    domain=domain, language=detected_lang, filename=clean_filename, source_url=link,
                    discovered_via="auto_crawl", status="downloaded", downloaded_at=now_str
                )
                
                # Trigger indexing pipeline
                page_count, chunk_count, index_status = kb_pipeline.index_document(
                    domain=domain, language=detected_lang, filename=clean_filename, source_url=link,
                    discovered_via="auto_crawl", file_path=final_path
                )
                print(f"Indexed auto-discovered file. Status: {index_status} (Chunks: {chunk_count})")
                
                downloaded_totals[domain] += 1
                
            except Exception as e:
                print(f"Error processing auto-discovered file: {e}")
                kb_pipeline.upsert_document_record(
                    domain=domain, language="unknown", filename=temp_filename, source_url=link,
                    discovered_via="auto_crawl", status="failed"
                )
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
    # Log crawler summary reports to console
    print("\n==========================================")
    print("Auto-Discovery Crawler Run Finished.")
    for domain in found_totals:
        print(f"Domain '{domain}': Found {found_totals[domain]} candidates, Downloaded/Indexed {downloaded_totals[domain]} (Cap: {MAX_AUTO_DOCS_PER_DOMAIN})")
    print("==========================================")

if __name__ == "__main__":
    main()
