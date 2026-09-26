# Mini Challenge 2 Submission Draft

## Title

InfraLens OCR: AMD Visual Asset Intelligence

## Long description

InfraLens OCR is an AMD ROCm-powered OCR system built for Mini Challenge 2 and designed to remain useful beyond the challenge. Its challenge adapter reads license plates and traffic signs under real-world conditions such as blur, glare, noise and off-axis camera angles. It follows task-specific normalization rules, including removing state names and slogans from US plates, preserving the province character on Chinese plates, joining multi-line road signs in reading order, and returning only the numeric value for advisory plaques.

The system runs in the mandated ROCm/PyTorch Docker environment and keeps an open-weights Qwen2.5-VL vision-language model resident in memory so each grader request is a lightweight local call rather than a full model reload. Bounded test-time augmentation improves difficult images while respecting the evaluation latency budget.

InfraLens also demonstrates how this OCR core can become useful infrastructure software. An optional Asset Passport mode converts equipment labels into structured fields such as model, serial number, MAC address and voltage, with an image hash for traceability. That extension is isolated from the grader-facing JSON, so challenge compliance remains strict while the same technology can later plug into InnerOS, FieldOps and Vigilos for real physical-asset inventory workflows.

## Suggested categories

Computer Vision; Developer Tools; Infrastructure; Productivity

## Technologies used

AMD ROCm; PyTorch; Qwen2.5-VL; Hugging Face; Docker; Python

## Mini Challenge 2 Image

Insert the final public container reference only after the exact pushed artifact passes the AMD GPU harness.
