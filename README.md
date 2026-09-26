# InfraLens OCR

AMD-powered OCR that turns pixels into structured physical-world data.

InfraLens OCR is built for the Lablab x AMD AI Academy Mini Challenge 2 and designed to remain useful after the challenge.

For the AMD grader, InfraLens provides a strict challenge adapter for license plates and traffic signs. For the InnerChispa / PC Doctor ecosystem, the same OCR core can optionally emit an Asset Passport sidecar for equipment labels, serial numbers, MAC addresses, models and electrical metadata.

## Challenge contract

Mandated base image:

    rocm/pytorch:rocm10.0_ubuntu26.04_py3.14_pytorch_release_2.13.0

The resident server loads the open-weights vision-language model once. The grader invokes:

    python3 /app/app.py --input-image /app/input/example.png --output-dir /app/output

Required output:

    {"text": "8ABC123", "confidence": 1.0}

The grader-facing JSON stays intentionally minimal. InfraLens product metadata is written only when --asset-passport is requested.

## Challenge behavior

- US license plates: registration characters only, excluding state/slogan text.
- Mainland Chinese plates: province character preserved.
- Multi-line road and work-zone signs: joined top-to-bottom.
- Numeric advisory plaques: number only, without units.
- Blur, glare and off-axis images: bounded test-time augmentation with majority voting.
- Runtime: model is resident so per-image calls do not reload weights.

## Product extension: Asset Passport

    photo -> OCR -> structured fields -> Asset Passport -> inventory / FieldOps / Vigilos

Optional extracted fields include model, serial, MAC address and voltage. Each Asset Passport also records a SHA-256 image fingerprint for traceability.

## Architecture

    AMD ROCm / PyTorch
            |
    Qwen2.5-VL-3B-Instruct
            |
       OCR core
        /    \
 challenge   InfraLens
 adapter     adapter
    |           |
{text,conf}  Asset Passport
    |           |
 AMD grader  InnerOS / FieldOps / Vigilos

## Local tests

These tests do not download the model:

    python3 -m pip install Pillow pytest
    pytest -q
    python3 scripts/test_contract.py

The deterministic OCR_MOCK_TEXT hook exists only for contract tests and is never set in the submitted Docker image.

## Submission gates

The final public container must be validated against the challenge limits before its registry reference is submitted:

- mandated ROCm base preserved and not squashed
- uncompressed image under 60 GiB
- startup under 10 minutes
- each image under 30 seconds
- full evaluation batch under 10 minutes
- peak VRAM between 1 and 48 GiB
- no tokens, keys or .env inside the image
- all output JSON files present

## Status

- public repository: created
- grader CLI contract: implemented
- challenge-specific post-processing: implemented
- optional Asset Passport: implemented
- CPU/mock validation: in progress
- final ROCm image build: pending
- final AMD GPU harness: pending

## License

MIT
