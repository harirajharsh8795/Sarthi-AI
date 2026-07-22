import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_PATTERNS = [
    r'(\b[A-Za-z0-9_]{16,}\b.*[0-9a-f]{32,})',
    r'API_KEY\s*=\s*["\'][A-Za-z0-9_\-]{20,}["\']',
    r'AWS_SECRET_ACCESS_KEY\s*=\s*["\'][A-Za-z0-9/+=]{40}["\']',
    r'-----BEGIN PRIVATE KEY-----'
]

def scan_secrets():
    print("[SECRET SCANNER] Scanning codebase for hardcoded secrets and API keys...")
    violations = []
    
    for root, dirs, files in os.walk(ROOT_DIR):
        if ".git" in root or "node_modules" in root or "backups" in root or "venv" in root:
            continue
        for file in files:
            if file.endswith((".py", ".json", ".env", ".yml", ".yaml")):
                fpath = os.path.join(root, file)
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                for pattern in SECRET_PATTERNS:
                    if re.search(pattern, content):
                        violations.append(f"{os.path.relpath(fpath, ROOT_DIR)} matches pattern {pattern}")

    if violations:
        print(f"[WARNING] Potential secrets detected in {len(violations)} files:")
        for v in violations:
            print(f" - {v}")
    else:
        print("[SECRET SCANNER PASSED] Zero hardcoded secrets detected.\n")

if __name__ == "__main__":
    scan_secrets()
