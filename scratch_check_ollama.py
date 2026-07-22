import requests
try:
    r = requests.get("http://localhost:11434/api/tags", timeout=3)
    if r.status_code == 200:
        print("OLLAMA_IS_RUNNING")
        data = r.json()
        models = [m['name'] for m in data.get('models', [])]
        print("Models:", models)
    else:
        print(f"OLLAMA_ERROR: {r.status_code}")
except Exception as e:
    print("OLLAMA_NOT_RESPONDING:", str(e))
