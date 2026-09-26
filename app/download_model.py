from __future__ import annotations
import os
from huggingface_hub import snapshot_download

model_id = os.environ.get("MODEL_ID", "Qwen/Qwen2.5-VL-3B-Instruct")
model_dir = os.environ["MODEL_DIR"]
snapshot_download(
    repo_id=model_id,
    local_dir=model_dir,
    local_dir_use_symlinks=False,
    allow_patterns=[
        "*.json","*.safetensors","*.model","*.txt","*.jinja",
        "tokenizer*","merges.txt","vocab.json","preprocessor_config.json"
    ]
)
print(model_dir)
