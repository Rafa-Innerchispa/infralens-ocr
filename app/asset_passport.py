from __future__ import annotations
import hashlib
import re
from pathlib import Path

PATTERNS = {
    "mac": re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b"),
    "serial": re.compile(r"\b(?:S/?N|SERIAL)\s*[:#-]?\s*([A-Z0-9-]{5,})\b", re.I),
    "model": re.compile(r"\b(?:MODEL|M/N)\s*[:#-]?\s*([A-Z0-9._/-]{3,})\b", re.I),
    "voltage": re.compile(r"\b(\d{1,3}(?:\.\d+)?\s*V(?:AC|DC)?)\b", re.I)
}

def image_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_asset_passport(path: str | Path, raw_text: str, confidence: float) -> dict:
    fields = {}
    for name, pattern in PATTERNS.items():
        match = pattern.search(raw_text or "")
        if match:
            fields[name] = match.group(1) if match.groups() else match.group(0)
    return {
        "schema": "infralens.asset_passport.v1",
        "image_sha256": image_sha256(path),
        "ocr_text": raw_text,
        "ocr_confidence": confidence,
        "fields": fields
    }
