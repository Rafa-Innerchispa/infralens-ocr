from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td_raw:
    td = Path(td_raw)
    img = td / "plate.png"
    im = Image.new("RGB", (600, 240), "white")
    ImageDraw.Draw(im).text((30, 80), "California 8ABC123", fill="black")
    im.save(img)
    env = os.environ.copy()
    env["OCR_MOCK_TEXT"] = "California 8ABC123"
    env["OCR_MOCK_TASK"] = "plate"
    env["PYTHONPATH"] = str(root / "app")
    p = subprocess.run(
        [sys.executable, str(root / "app/app.py"), "--input-image", str(img), "--output-dir", str(td)],
        env=env, text=True, capture_output=True
    )
    assert p.returncode == 0, (p.stdout, p.stderr)
    result = json.loads((td / "plate_output.json").read_text())
    assert result["text"] == "8ABC123", result
    assert 0 <= result["confidence"] <= 1
print("contract PASS")
