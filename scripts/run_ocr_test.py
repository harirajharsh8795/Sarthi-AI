import shutil
import os
import traceback

def main():
    import sys
    # Ensure workspace root is on sys.path so sibling packages (backend) can be imported
    workspace_root = os.getcwd()
    if workspace_root not in sys.path:
        sys.path.insert(0, workspace_root)
    backend_dir = os.path.join(workspace_root, 'backend')
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    print('CWD:', workspace_root)
    print('sys.path[0:5]:', sys.path[0:5])
    src = r"e:/Desktop/Saarthi AI/test_documents/medical.pdf"
    tmp = r"e:/Desktop/Saarthi AI/temp_medical_for_test.pdf"
    print('Copying', src, '->', tmp)
    shutil.copy(src, tmp)

    try:
        from backend import kb_pipeline
        print('Calling ingest_user_document...')
        res = kb_pipeline.ingest_user_document(tmp, "medical.pdf", "session_test_local")
        print('Ingest result:')
        print(res)
    except Exception:
        print('Exception during ingestion:')
        traceback.print_exc()

if __name__ == '__main__':
    main()
