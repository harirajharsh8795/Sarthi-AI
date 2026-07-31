import sys
import os

def main(doc_id):
    workspace_root = os.getcwd()
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)
    backend_dir = os.path.join(workspace_root, 'backend')
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    from backend import services

    collection = services.chroma_manager.get_collection('user_docs')

    # Query by metadata document_id
    results = collection.get(where={'document_id': doc_id}, include=['metadatas', 'documents'])
    docs = results.get('documents') if isinstance(results, dict) else None
    print('Query results type:', type(results))
    try:
        metadatas = results.get('metadatas', [])
        documents = results.get('documents', [])
        for i, (m, d) in enumerate(zip(metadatas, documents)):
            print('--- Chunk', i, 'page:', m.get('page_number'), 'chunk:', m.get('chunk_index'))
            print('meta:', m)
            safe_text = (d or '')[:300].replace('\n',' ').encode('ascii', 'backslashreplace').decode('ascii')
            print('text excerpt (ascii-safe):', safe_text)
            print()
    except Exception as e:
        print('Could not pretty-print results:', e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python check_indexed_doc.py <document_id>')
        sys.exit(1)
    main(sys.argv[1])
