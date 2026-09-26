from __future__ import annotations
import json
import os
import time
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from config import MODEL_DIR, MODEL_ID, OCR_DTYPE, OCR_MAX_NEW_TOKENS, OCR_MAX_PIXELS, OCR_TIME_BUDGET_S, OCR_TTA_PASSES
from postprocess import normalize_output

PROMPT = """You are an OCR engine for an AMD evaluation.
Return ONLY one JSON object: {"task":"plate|sign|unknown","text":"..."}.
For a license plate, return only registration characters.
For US plates, exclude state names, slogans, websites, stickers and decorative text.
For mainland Chinese plates, preserve the province character.
For a traffic sign, return only meaningful sign text.
Join multi-line signs top-to-bottom with single spaces.
For numeric advisory plaques, return only the number without units.
Ignore borders, logos and unrelated scene text.
Never invent missing characters. No markdown or explanation."""

class OCREngine:
    def __init__(self) -> None:
        self.model = None
        self.processor = None
        self.loaded_at = None

    def load(self) -> None:
        if self.loaded_at is not None:
            return
        if os.getenv("OCR_MOCK_TEXT") is not None:
            self.loaded_at = time.time()
            return
        import torch
        from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
        dtype_map = {"bf16": torch.bfloat16, "fp16": torch.float16, "fp32": torch.float32}
        dtype = dtype_map.get(OCR_DTYPE, torch.bfloat16)
        source = MODEL_DIR if Path(MODEL_DIR).exists() else MODEL_ID
        local = Path(MODEL_DIR).exists()
        self.processor = AutoProcessor.from_pretrained(
            source, min_pixels=256 * 28 * 28, max_pixels=OCR_MAX_PIXELS,
            local_files_only=local
        )
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            source, torch_dtype=dtype, device_map="auto", local_files_only=local
        )
        self.model.eval()
        self.loaded_at = time.time()

    @staticmethod
    def variants(image: Image.Image) -> list[Image.Image]:
        rgb = image.convert("RGB")
        auto = ImageOps.autocontrast(rgb)
        sharp = ImageEnhance.Sharpness(auto).enhance(1.8)
        denoise = sharp.filter(ImageFilter.MedianFilter(size=3))
        return [rgb, sharp, denoise]

    def _generate_once(self, image: Image.Image) -> tuple[str, str]:
        mock = os.getenv("OCR_MOCK_TEXT")
        if mock is not None:
            return os.getenv("OCR_MOCK_TASK", "unknown"), mock
        import torch
        from qwen_vl_utils import process_vision_info
        messages = [{"role":"user","content":[
            {"type":"image","image":image},
            {"type":"text","text":PROMPT}
        ]}]
        prompt = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[prompt], images=image_inputs, videos=video_inputs,
            padding=True, return_tensors="pt"
        ).to(self.model.device)
        with torch.inference_mode():
            generated = self.model.generate(
                **inputs, max_new_tokens=OCR_MAX_NEW_TOKENS, do_sample=False
            )
        trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, generated)]
        raw = self.processor.batch_decode(
            trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )[0].strip()
        try:
            payload = json.loads(raw)
            return str(payload.get("task","unknown")), str(payload.get("text",""))
        except Exception:
            return "unknown", raw.strip()

    def predict(self, image_path: str) -> dict[str, Any]:
        self.load()
        image = Image.open(image_path)
        started = time.monotonic()
        candidates = []
        for variant in self.variants(image)[:OCR_TTA_PASSES]:
            if candidates and time.monotonic() - started >= OCR_TIME_BUDGET_S:
                break
            task, text = self._generate_once(variant)
            candidates.append((task, normalize_output(text, task)))
        if not candidates:
            return {"text":"","confidence":0.0,"task":"unknown","passes":0}
        counts = Counter(text for _, text in candidates)
        winner, votes = counts.most_common(1)[0]
        task = next(t for t, text in candidates if text == winner)
        return {
            "text": winner,
            "confidence": round(votes / len(candidates), 4),
            "task": task,
            "passes": len(candidates)
        }

    def warmup(self) -> None:
        self.load()
