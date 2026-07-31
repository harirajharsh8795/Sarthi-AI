import os, sys
workspace_root = os.getcwd()
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)
backend_dir = os.path.join(workspace_root,'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from backend import services

session_id = 'session_test_local'
conversation_id = ''
query = 'explain my report'

# 1. Get embedding for the query
model = services.embedding_service.get_model()
vec = model.encode([query], show_progress_bar=False)[0]

# 2. Query user docs
res = services.rag_service.embed_and_query_user_docs(session_id, conversation_id, vec, n=5)
print('RAG query result keys:', list(res.keys()))
# res format: dict with 'documents','metadatas','distances'
docs = res.get('documents', [[]])[0]
metas = res.get('metadatas', [[]])[0]
dists = res.get('distances', [[]])[0]
print('Retrieved', len(docs), 'chunks')
for i, (d, m, dist) in enumerate(zip(docs, metas, dists)):
    print('---', i, 'page:', m.get('page_number'), 'chunk:', m.get('chunk_index'), 'dist:', dist)
    safe_d = (d or '')[:400].replace('\n',' ').encode('ascii','backslashreplace').decode('ascii')
    print(safe_d)
    print()
