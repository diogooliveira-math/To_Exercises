import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
from fastapi.testclient import TestClient
from to_exercises.main import app
client = TestClient(app)
payload = {"title":"Dup exercise","checksum":"abc123","content":"x"}
r = client.post('/exercises', json=payload)
print('status', r.status_code)
try:
    print('json:', r.json())
except Exception:
    print('text:', r.text)
