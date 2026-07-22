import pytest
import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="module")
def session_id():
    # Create a session
    resp = requests.post(f"{BASE_URL}/api/session", json={"display_name": "Acceptance Test User"})
    assert resp.status_code == 200
    data = resp.json()
    assert "session_id" in data
    return data["session_id"]

def test_health():
    resp = requests.get(f"{BASE_URL}/api/health")
    assert resp.status_code == 200

def test_system_resources():
    resp = requests.get(f"{BASE_URL}/api/system/resources")
    assert resp.status_code == 200

def test_system_cache():
    resp = requests.get(f"{BASE_URL}/api/system/cache")
    assert resp.status_code == 200

def test_system_performance():
    resp = requests.get(f"{BASE_URL}/api/system/performance")
    assert resp.status_code == 200

def test_system_deployment():
    resp = requests.get(f"{BASE_URL}/api/system/deployment")
    assert resp.status_code == 200

def test_system_diagnostics():
    resp = requests.get(f"{BASE_URL}/api/system/diagnostics")
    assert resp.status_code == 200

def test_observability():
    resp = requests.get(f"{BASE_URL}/api/observability")
    assert resp.status_code == 200

def test_security_status():
    resp = requests.get(f"{BASE_URL}/api/security/status")
    assert resp.status_code == 200

def test_security_audit():
    resp = requests.get(f"{BASE_URL}/api/security/audit")
    assert resp.status_code == 200

def test_security_compliance():
    resp = requests.get(f"{BASE_URL}/api/security/compliance")
    assert resp.status_code == 200

def test_security_trust():
    resp = requests.get(f"{BASE_URL}/api/security/trust")
    assert resp.status_code == 200

def test_security_production():
    resp = requests.get(f"{BASE_URL}/api/security/production")
    assert resp.status_code == 200

def test_chat_stream(session_id):
    # Test chat streaming endpoint
    query = "Hello, what can you do?"
    url = f"{BASE_URL}/api/stream?query={query}&session_id={session_id}&response_language=English"
    # Stream the response
    resp = requests.get(url, stream=True)
    assert resp.status_code == 200
    # Just read the first few bytes to ensure it's streaming SSE
    for line in resp.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            assert decoded_line.startswith("data:")
            break

def test_conversations_list(session_id):
    resp = requests.get(f"{BASE_URL}/api/conversations?session_id={session_id}")
    assert resp.status_code == 200
    assert "conversations" in resp.json()

def test_history(session_id):
    resp = requests.get(f"{BASE_URL}/api/history?session_id={session_id}")
    assert resp.status_code == 200
    assert "documents" in resp.json()

def test_search_messages(session_id):
    resp = requests.get(f"{BASE_URL}/api/search/messages?q=test&session_id={session_id}")
    assert resp.status_code in [200, 404] # Might be empty but shouldn't 500
