from __future__ import annotations
import json
import urllib.request
from config import OCR_PORT

try:
    with urllib.request.urlopen(f"http://127.0.0.1:{OCR_PORT}/health", timeout=3) as r:
        payload = json.loads(r.read().decode("utf-8"))
    raise SystemExit(0 if payload.get("ok") and payload.get("model_loaded") else 1)
except Exception:
    raise SystemExit(1)
