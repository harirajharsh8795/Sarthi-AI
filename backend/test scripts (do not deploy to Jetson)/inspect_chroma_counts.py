import chromadb

def main():
    client = chromadb.PersistentClient(path="./data/chroma_db")
    col = client.get_collection("knowledge_base")
    
    domains = {}
    offset = 0
    limit = 5000
    
    while True:
        res = col.get(limit=limit, offset=offset, include=["metadatas"])
        metas = res["metadatas"]
        if not metas:
            break
        for m in metas:
            d = m.get("domain", "unknown")
            domains[d] = domains.get(d, 0) + 1
        offset += limit
        
    print("Actual ChromaDB domains breakdown:")
    for domain, count in domains.items():
        print(f"  {domain} domain: {count} chunks")

if __name__ == "__main__":
    main()
