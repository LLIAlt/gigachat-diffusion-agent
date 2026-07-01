# FLUX.1 [dev]

## Metadata

Model Name: FLUX.1 [dev]

Developer: Black Forest Labs

Model Type: Text-to-Image

Architecture: Rectified Flow Transformer

Parameter Count: ~12B

License: Non-commercial

Primary Use Cases:

* Photorealistic image generation
* Concept art
* Character design
* Environmental scenes
* Product visualization

---

# Overview

FLUX.1 [dev] is a high-quality open-weight diffusion model based on Rectified Flow Transformer architecture.

The model demonstrates strong prompt adherence, realistic lighting, natural composition, and detailed image generation while maintaining relatively low CFG requirements compared to traditional diffusion models.

FLUX.1 [dev] generally performs best when prompts prioritize concrete visual descriptions over abstract artistic language.

---

# Architecture Notes

## Rectified Flow

Unlike traditional diffusion models, FLUX uses flow matching / rectified flow techniques.

Practical implications:

* Lower CFG values are usually sufficient
* Prompt structure matters significantly
* Early tokens receive stronger weighting
* Prompt clarity often matters more than prompt length

---

# Prompting Guidelines

## Recommended Structure

For subject-focused scenes:

[SUBJECT]
[ACTION]
[ENVIRONMENT]
[ATMOSPHERE]
[STYLE]
[TECHNICAL DETAILS]

Example:

"A medieval knight, standing on a rocky cliff, overlooking a stormy sea, dramatic atmosphere, cinematic photography, 35mm lens"

---

## Subject Priority

FLUX assigns greater importance to earlier prompt tokens.

Recommended:

"A red fox sitting in snow, winter forest"

Avoid:

"Winter forest with trees and snow where a red fox is sitting"

if the fox is intended to be the primary subject.

---

## Style Modifiers

Recommended:
1–2 style modifiers

Acceptable:
3 style modifiers

Not recommended:
4+ style modifiers

Observed behavior:

Excessive style modifiers may produce style averaging effects rather than additive stylistic control.

Example:

"cinematic, oil painting, watercolor, anime, photorealistic"

can lead to mixed visual output.

---

# Recommended Generation Settings

## General Purpose

Steps:
24–30

CFG:
3.0–3.5

Resolution:
1024x1024

---

## Portraits

Steps:
22–28

CFG:
3.0

Recommended Samplers:

* Euler
* Euler Ancestral
* DPM++ 2M

---

## Complex Anatomy

Examples:

* holding objects
* hands visible
* dynamic poses
* multiple characters

Steps:
30–35

CFG:
3.5

Additional Prompt Guidance:

"five fingers on each hand, anatomically correct hands, natural joint articulation"

---

## Environment Scenes

Steps:
20–28

CFG:
2.8–3.2

Additional Prompt Guidance:

"distinct foreground, defined midground, atmospheric perspective"

---

## Composite Scenes

Subject and environment equally important.

Steps:
32–38

CFG:
3.5

---

# Strengths

## Prompt Adherence

FLUX follows detailed prompts accurately.

Particularly effective with:

* object descriptions
* environmental details
* cinematic compositions

---

## Natural Lighting

Strong performance in:

* golden hour lighting
* volumetric lighting
* realistic shadows
* atmospheric effects

---

## Composition

Produces coherent framing and scene layout with minimal prompt engineering.

---

## Realism

Strong results in:

* skin textures
* clothing materials
* architectural details
* environmental rendering

---

# Known Limitations

## Character Consistency

Confidence:
High

Description:

Character identity does not reliably persist between separate generations.

Recommended Solution:

Use:

* reference workflows
* IPAdapter
* character LoRAs

---

## Style Averaging

Confidence:
High

Description:

Multiple competing artistic styles may blend together.

Symptoms:

* weak style identity
* inconsistent rendering

Recommended Solution:

Limit style modifiers to 1–3.

---

## High CFG Degradation

Confidence:
High

Description:

CFG above 4.5 frequently introduces visual degradation.

Symptoms:

* over-contrasted images
* crushed shadows
* glowing highlights
* harsh edges

Recommended Solution:

Reduce CFG to 3.0–4.0.

---

## Hand Anatomy Failures

Confidence:
Medium

Description:

Complex hand-object interactions may occasionally produce:

* fused fingers
* incorrect finger counts
* malformed hands

Recommended Solution:

Explicit anatomy reinforcement in prompt.

Example:

"five fingers on each hand, detailed knuckles, anatomically correct hands"

---

# Troubleshooting Guide

## Problem: Plastic Skin

Possible Causes:

* excessive realism modifiers
* high CFG
* over-processed LoRA stack

Recommended Fixes:

* reduce CFG
* simplify style instructions
* reduce LoRA strength

---

## Problem: Overcooked Contrast

Possible Causes:

* CFG above 4.5

Fix:

CFG 3.0–3.5

---

## Problem: Weak Subject Focus

Possible Causes:

* important subject placed late in prompt

Fix:

Move subject description to beginning of prompt.

---

## Problem: Inconsistent Style

Possible Causes:

* too many style modifiers

Fix:

Reduce to one dominant style.

---

# ComfyUI Recommendations

## Basic Workflow

Load Checkpoint
→ CLIP Text Encode
→ Empty Latent Image
→ KSampler
→ VAE Decode
→ Save Image

---

## Portrait Workflow

Load Checkpoint
→ LoRA Loader
→ CLIP Encode
→ KSampler
→ Face Detailer
→ VAE Decode

---

## High Quality Workflow

Load Checkpoint
→ CLIP Encode
→ KSampler
→ Latent Upscale
→ Second KSampler
→ VAE Decode

---

# Hardware Requirements

## Minimum

GPU VRAM:
12 GB

Examples:

* RTX 3060 12GB

---

## Comfortable

GPU VRAM:
16–24 GB

Examples:

* RTX 4080
* RTX 4090

---

# Best Practices

1. Place the primary subject first.
2. Use concrete nouns instead of abstract adjectives.
3. Keep style modifiers below three.
4. Use CFG between 3.0 and 4.0.
5. Explicitly reinforce anatomy when hands are important.
6. Add depth cues for landscapes.
7. Use clear scene hierarchy.

---

# Sources

Official Model Card:
https://huggingface.co/black-forest-labs/FLUX.1-dev

Developer:
https://blackforestlabs.ai

GitHub:
https://github.com/black-forest-labs

ComfyUI:
https://github.com/comfyanonymous/ComfyUI

Last Updated:
2026-02