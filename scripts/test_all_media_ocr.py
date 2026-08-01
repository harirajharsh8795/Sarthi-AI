import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
import kb_pipeline

brain_dir = r"C:\Users\HP\.gemini\antigravity-ide\brain\f75faf6d-afdc-47e5-94dd-6e2ace58324c"

for fname in os.listdir(brain_dir):
    if fname.endswith(".png") or fname.endswith(".webp"):
        fpath = os.path.join(brain_dir, fname)
        text = kb_pipeline.extract_text_from_image_ocr(fpath)
        print(f"\n==================== {fname} ====================")
        print(text[:300] if text else "EMPTY TEXT!")
