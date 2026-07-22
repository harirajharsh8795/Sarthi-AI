import requests
import json
import base64
import time

base_url = "http://localhost:8000"

def test_retrieval_isolation():
    r = requests.get(f"{base_url}/api/conversations?session_id=test_session_2")
    conversations = r.json().get("conversations", [])
    convB_id = None
    for c in conversations:
        if c["title"] == "Conv B":
            convB_id = c["id"]
    
    if not convB_id:
        print("Conv B not found!")
        return

    print(f"Testing stream endpoint for ConvB ({convB_id})")
    
    r = requests.get(f"{base_url}/api/stream?query=What%20is%20in%20the%20image%3F&session_id=test_session_2&conversation_id={convB_id}")
    print("ConvB Stream HTTP Status:", r.status_code)
    
    for line in r.iter_lines():
        if line:
            print(line.decode('utf-8'))

if __name__ == "__main__":
    test_retrieval_isolation()
