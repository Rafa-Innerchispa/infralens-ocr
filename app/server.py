from __future__ import annotations
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from config import OCR_PORT
from ocr_engine import OCREngine

engine = OCREngine()
engine.warmup()

class Handler(BaseHTTPRequestHandler):
    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"ok": True, "model_loaded": engine.loaded_at is not None})
        else:
            self._json(404, {"ok": False})

    def do_POST(self) -> None:
        if self.path != "/ocr":
            self._json(404, {"ok": False})
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            request = json.loads(self.rfile.read(size).decode("utf-8"))
            path = request["input_image"]
            if not os.path.isfile(path):
                raise FileNotFoundError(path)
            self._json(200, {"ok": True, "result": engine.predict(path)})
        except Exception as exc:
            self._json(500, {"ok": False, "error": f"{type(exc).__name__}: {exc}"})

    def log_message(self, fmt: str, *args) -> None:
        return

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", OCR_PORT), Handler).serve_forever()
