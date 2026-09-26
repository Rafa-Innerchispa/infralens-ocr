from __future__ import annotations
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

from asset_passport import build_asset_passport
from config import OCR_PORT
from ocr_engine import OCREngine

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="InfraLens OCR challenge client")
    p.add_argument("--input-image", required=True)
    p.add_argument("--output-dir", default="/app/output")
    p.add_argument("--asset-passport", action="store_true")
    return p.parse_args()

def call_server(image: str) -> dict:
    body = json.dumps({"input_image": image}).encode("utf-8")
    req = urllib.request.Request(
        f"http://127.0.0.1:{OCR_PORT}/ocr",
        data=body, headers={"Content-Type":"application/json"}, method="POST"
    )
    with urllib.request.urlopen(req, timeout=35) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not payload.get("ok"):
        raise RuntimeError(payload.get("error", "OCR server failed"))
    return payload["result"]

def run_local(image: str) -> dict:
    return OCREngine().predict(image)

def main() -> int:
    args = parse_args()
    src = Path(args.input_image)
    if not src.is_file():
        print(f"Input image not found: {src}", file=sys.stderr)
        return 2
    try:
        result = call_server(str(src))
    except Exception:
        result = run_local(str(src))
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    challenge_path = outdir / f"{src.stem}_output.json"
    challenge = {
        "text": str(result.get("text","")),
        "confidence": float(result.get("confidence",0.0))
    }
    challenge_path.write_text(json.dumps(challenge, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.asset_passport or os.getenv("INFRALENS_ASSET_PASSPORT") == "1":
        asset = build_asset_passport(src, challenge["text"], challenge["confidence"])
        (outdir / f"{src.stem}_asset.json").write_text(
            json.dumps(asset, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(str(challenge_path))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
