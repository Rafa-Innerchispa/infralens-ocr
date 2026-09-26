from __future__ import annotations
import os

MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-VL-3B-Instruct")
MODEL_DIR = os.getenv("MODEL_DIR", f"/models/{MODEL_ID.rsplit('/', 1)[-1]}")
OCR_PORT = int(os.getenv("OCR_PORT", "8765"))
OCR_TTA_PASSES = max(1, min(3, int(os.getenv("OCR_TTA_PASSES", "3"))))
OCR_TIME_BUDGET_S = float(os.getenv("OCR_TIME_BUDGET_S", "20"))
OCR_MAX_NEW_TOKENS = int(os.getenv("OCR_MAX_NEW_TOKENS", "48"))
OCR_MAX_PIXELS = int(os.getenv("OCR_MAX_PIXELS", "1003520"))
OCR_DTYPE = os.getenv("OCR_DTYPE", "bf16").lower()
