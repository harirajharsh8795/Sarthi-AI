import requests
import json
import base64

base_url = "http://localhost:8000"

def test_upload_and_history():
    # Create session
    requests.post(f"{base_url}/api/session", json={"session_id": "test_session_2", "display_name": "Test"})
    
    # Create conversation A
    r_convA = requests.post(f"{base_url}/api/conversations", json={"session_id": "test_session_2", "title": "Conv A"})
    convA_id = r_convA.json()["conversation_id"]
    
    # Create conversation B
    r_convB = requests.post(f"{base_url}/api/conversations", json={"session_id": "test_session_2", "title": "Conv B"})
    convB_id = r_convB.json()["conversation_id"]
    
    # Upload to A
    png_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=")
    files = {"file": ("test.png", png_data, "image/png")}
    data = {"session_id": "test_session_2", "conversation_id": convA_id}
    r = requests.post(f"{base_url}/api/upload", files=files, data=data)
    print("Upload Response:", r.status_code, r.text)
    
    # Check history
    r = requests.get(f"{base_url}/api/history?session_id=test_session_2&conversation_id={convA_id}")
    print("ConvA History:", json.dumps(r.json(), indent=2))
    
    r = requests.get(f"{base_url}/api/history?session_id=test_session_2&conversation_id={convB_id}")
    print("ConvB History:", json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    test_upload_and_history()
