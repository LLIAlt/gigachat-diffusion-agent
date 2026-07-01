# Qwen Image

## Overview

Developer: Alibaba / Qwen Team

Architecture:
MMDiT

Primary Use Cases:
- Illustration
- Posters
- Typography
- General image generation

## Recommended Settings

Quality:
- Steps: 50
- CFG: 3.5-5.0

Lightning:
- Steps: 4-8
- CFG: 1.0

## Strengths

- Excellent text rendering
- Strong prompt understanding
- High detail

## Weaknesses

- Oversaturation tendency
- Grid artifacts on aggressive quantization
- Style conflicts when too many modifiers are used

## Troubleshooting

Problem:
Oversaturated image

Solution:
Add:
"natural color grading, balanced saturation"

Problem:
Grid artifacts

Possible Causes:
- Q4 quantization
- FP8 + LoRA combination

## Prompting Notes

- Maximum 2 style modifiers
- Explicitly specify text placement
- Prefer concrete object descriptions

## Sources

HF:
https://huggingface.co/Qwen/Qwen-Image