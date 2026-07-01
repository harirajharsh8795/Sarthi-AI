import os
import json
import sqlite3
import kb_pipeline

def generate_report():
    print("Generating Stage 0 Knowledge Base Seeding Report...")
    
    # 1. Query SQLite documents
    try:
        conn = kb_pipeline.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT domain, language, filename, discovered_via, status, page_count, chunk_count FROM kb_documents")
        rows = cursor.fetchall()
        conn.close()
        documents = [dict(r) for r in rows]
    except Exception as e:
        print(f"Error reading SQLite database: {e}")
        documents = []
        
    # 2. Query ChromaDB count
    chroma_count = 0
    chroma_status = "Not initialized"
    try:
        collection = kb_pipeline.get_chroma_collection()
        chroma_count = collection.count()
        chroma_status = "Active and PersistentClient verified"
    except Exception as e:
        chroma_status = f"Error: {e}"
        
    # 3. Read glossary count
    glossary_count = 0
    glossary_status = "Not found"
    try:
        glossary_path = os.path.join(".", "glossary", "hinglish_medical_terms.json")
        if os.path.exists(glossary_path):
            with open(glossary_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                glossary_count = len(data)
                glossary_status = "Successfully created and loaded"
    except Exception as e:
        glossary_status = f"Error: {e}"
        
    # 4. Process metrics
    total_downloaded = 0
    total_failed = 0
    failed_reasons = []
    
    # Domain and language counts
    domain_chunks = {}
    lang_chunks = {}
    
    table_lines = []
    # Table Header
    header = f"{'Domain':<30} | {'Lang':<5} | {'Source':<10} | {'Status':<15} | {'Pages':<5} | {'Chunks':<5} | {'Filename':<35}"
    separator = "-" * len(header)
    table_lines.append(header)
    table_lines.append(separator)
    
    for doc in documents:
        domain = doc["domain"]
        lang = doc["language"]
        filename = doc["filename"]
        source = "seed" if doc["discovered_via"] == "seed_list" else "auto_crawl"
        status = doc["status"]
        pages = doc["page_count"] if doc["page_count"] is not None else 0
        chunks = doc["chunk_count"] if doc["chunk_count"] is not None else 0
        
        # Format filename to fit nicely if too long
        display_filename = filename
        if len(display_filename) > 35:
            display_filename = display_filename[:32] + "..."
            
        row_str = f"{domain:<30} | {lang:<5} | {source:<10} | {status:<15} | {pages:<5} | {chunks:<5} | {display_filename:<35}"
        table_lines.append(row_str)
        
        # Aggregations
        if status in ["downloaded", "indexed", "skipped_exists"]:
            total_downloaded += 1
        elif status == "failed":
            total_failed += 1
            failed_reasons.append(filename)
            
        # Count only if chunks are indexed
        if status in ["indexed", "downloaded", "skipped_exists"] and chunks > 0:
            domain_chunks[domain] = domain_chunks.get(domain, 0) + chunks
            lang_chunks[lang] = lang_chunks.get(lang, 0) + chunks
            
    # Compile report text
    report_parts = [
        "=========================================================================",
        "                 SAARTHI AI - STAGE 0 SEEDING FINAL REPORT               ",
        "=========================================================================",
        "",
        "## ATTEMPTED DOCUMENTS TABLE",
        "",
        "\n".join(table_lines),
        "",
        "## AGGREGATE SUMMARY",
        f"Total documents successfully processed: {total_downloaded}",
        f"Total documents failed to process:      {total_failed}",
        f"Total chunks indexed into ChromaDB:     {chroma_count}",
        "",
        "### Chunk Breakdown by Domain:",
    ]
    
    for d, count in domain_chunks.items():
        report_parts.append(f"  - {d}: {count} chunks")
    if not domain_chunks:
        report_parts.append("  - None")
        
    report_parts.append("")
    report_parts.append("### Chunk Breakdown by Language:")
    for l, count in lang_chunks.items():
        report_parts.append(f"  - {l}: {count} chunks")
    if not lang_chunks:
        report_parts.append("  - None")
        
    report_parts.extend([
        "",
        "## INFRASTRUCTURE AND COMPLIANCE CHECKS",
        f"- ChromaDB Persist Directory:    {kb_pipeline.CHROMA_DIR}",
        f"- ChromaDB Status:               {chroma_status}",
        f"- ChromaDB Collection Size:      {chroma_count} chunks",
        f"- SQLite Database Path:          {kb_pipeline.DB_PATH}",
        f"- Glossary File Path:            ./glossary/hinglish_medical_terms.json",
        f"- Glossary Status:               {glossary_status} ({glossary_count} terms)",
        "",
        "========================================================================="
    ])
    
    report_content = "\n".join(report_parts)
    
    # Write to seed_report.txt
    report_path = os.path.join(kb_pipeline.DATA_DIR, "seed_report.txt")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"Report written successfully to {report_path}")
    except Exception as e:
        print(f"Error writing report file: {e}")
        
    # Also print to console
    print("\n" + report_content)

if __name__ == "__main__":
    generate_report()
