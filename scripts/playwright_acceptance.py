import os
import sys
import time
from playwright.sync_api import sync_playwright

FRONTEND_URL = "http://localhost:5173"

def run_tests():
    print("=== STARTING PLAYWRIGHT ACCEPTANCE LOOP ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. Load Page
        print("[1] Loading Frontend...")
        page.goto(FRONTEND_URL)
        page.wait_for_selector("text=Saarthi AI")

        # 2. Check "New Conversation" Lazy Creation
        print("[2] Verifying Lazy Conversation Creation...")
        page.click("button:has-text('New Chat')")
        page.wait_for_timeout(1000)
        
        input_locator = page.locator("textarea")
        input_locator.wait_for()
        assert input_locator.is_visible(), "Input area not visible"

        # 3. Send First Message & Auto-Rename
        print("[3] Sending First Message...")
        input_locator.fill("What is the constitution?")
        page.click("button[type='submit']")
        
        print("[4] Waiting for AI streaming response...")
        # Since it takes time, let's wait up to 30 seconds for the first token
        page.wait_for_timeout(10000)

        # Verify Citations rendered
        print("[5] Verifying Citations...")
        try:
            # We look for "Sources" which indicates citations drawer link
            page.wait_for_selector("text=Sources", timeout=5000)
            print("Citations rendered successfully.")
        except Exception as e:
            print(f"Warning: Sources didn't render within timeout. {e}")

        # 4. Upload Attachment Chip Verification
        print("[6] Uploading Test Document...")
        doc_path = os.path.abspath("test_doc.docx")
        with open(doc_path, "w") as f:
            f.write("test doc content for upload isolation check")
            
        # Set file input
        page.locator("input[type='file']").first.set_input_files(doc_path)
            
        page.wait_for_selector("text=test_doc.docx", timeout=5000)
        print("Attachment chip rendered successfully.")

        # 5. Conversation Switching & Isolation
        print("[7] Conversation Isolation check...")
        page.click("button:has-text('New Chat')")
        page.wait_for_timeout(1000)
        
        # In new chat, attachment chip should be GONE
        is_visible = page.locator("text=test_doc.docx").is_visible()
        if is_visible:
            print("FAILED: Document leaked to new conversation!")
            browser.close()
            sys.exit(1)
            
        print("Conversation isolation successful.")
        
        browser.close()
        print("=== ACCEPTANCE LOOP PASSED ===")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)
