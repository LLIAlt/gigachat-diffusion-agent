# Diffusion Model Assistant — LLM Query Router

A production-ready conversational agent that routes user queries to specialized knowledge bases using GigaChat API. Built to demonstrate applied prompt engineering techniques for real-world LLM workflows.

---

## What it does

The user asks a question about diffusion models. The agent:

1. **Routes** the query using zero-shot LLM classification (FLUX or Qwen)
2. **Loads** the matching knowledge base from disk
3. **Generates** a context-aware response using GigaChat

```
User: "What sampler should I use for portrait generation?"
        ↓
   router.py → classifies: "flux"
        ↓
   loads: knowledge/flux1[dev]info.md
        ↓
   GigaChat → generates expert answer with FLUX context
```

---

## Architecture

```
├── main.py           # Entry point — orchestrates the full pipeline
├── router.py         # Zero-shot intent classifier (routes to flux / qwen)
├── retry.py          # Shared retry wrapper with exponential backoff
├── ab_test.py        # A/B testing framework for prompt comparison
├── prompts/
│   ├── router.md     # Active router prompt (winner of A/B test)
│   ├── router_b.md   # Variant B — available for comparison
│   └── DMassistant.md  # Main assistant system prompt
├── knowledge/
│   ├── flux1[dev]info.md     # FLUX.1 [dev] knowledge base
│   ├── flux.schnellinfo.md   # FLUX Schnell knowledge base
│   └── qwen-imageinfo.md     # Qwen Image knowledge base
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Prompt Engineering techniques demonstrated

| Technique | Where | Description |
|-----------|-------|-------------|
| Zero-shot classification | `router.py` | Routes queries without examples |
| Output format control | `router.md` | Forces single-word lowercase response |
| Context injection | `main.py` | Appends knowledge base to system prompt |
| Parameter tuning | `router.py` / `main.py` | `temperature=0.0` for routing, `0.7` for generation |
| A/B prompt testing | `ab_test.py` | Measures accuracy across 8 test cases |
| Retry + exponential backoff | `retry.py` | Handles rate limits and server errors |
| Fallback routing | `main.py` | Logs unknown routes, proceeds gracefully |
| Structured logging | all files | Timestamps, levels, module names |

---

## A/B Test Results

Ran `ab_test.py` to compare two router prompt variants on 8 test cases:

```
=== Prompt A (router.md) — 100% ===
✅ I wanna generate image of old man          → flux
✅ How to set up FLUX for portrait generation  → flux
✅ What sampler should I use in FLUX?          → flux
✅ Which model is better for anime style?      → qwen
✅ How does Qwen handle image prompts?         → qwen
✅ I want to generate a landscape photo        → flux
✅ Tell me about Qwen image parameters         → qwen
✅ Best settings for photorealistic output     → flux

=== Prompt B (router_b.md) — 75% ===
❌ I wanna generate image of old man          → qwen (incorrect)
✅ How to set up FLUX for portrait generation  → flux
...

WINNER: Prompt A — 100% vs 75%
```

**Key insight:** The simpler, more direct prompt outperformed the more detailed variant. Concise output constraints (`reply with one lowercase word only`) proved more reliable than extended classification criteria.

---

## Setup

### Requirements

- Python 3.11+
- GigaChat API credentials (get at [developers.sber.ru](https://developers.sber.ru))
- Russian Trusted Root CA certificate (for SSL, see note below)

### Installation

```bash
git clone https://github.com/LLIAlt/diffusion-prompt-engineering
cd diffusion-prompt-engineering

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
GIGACHAT_CREDENTIALS=your_credentials_here
GIGACHAT_SCOPE=GIGACHAT_API_PERS
```

### SSL Certificate (Russia-specific)

GigaChat uses a Russian Ministry of Digital Development SSL certificate. If you encounter `CERTIFICATE_VERIFY_FAILED`:

```bash
# Download and add to certifi (Linux/Mac)
curl -k "https://gu-st.ru/content/Other/doc/russian_trusted_root_ca.cer" \
  -w "\n" >> $(python -m certifi)
```

For Windows/PowerShell:
```powershell
Invoke-WebRequest -Uri "https://gu-st.ru/content/Other/doc/russian_trusted_root_ca.cer" `
  -OutFile "russian_trusted_root_ca.cer" -SkipCertificateCheck
```

Alternatively, the client is currently configured with `verify_ssl_certs=False` for local development.

### Run

```bash
# Main agent
python main.py

# A/B prompt comparison
python ab_test.py
```

---

## Example output

```
> I want to generate a portrait of an old man, which model should I use?

2026-07-01 02:15:30 [INFO] main: User input received: 'I want to generate a portrait...'
2026-07-01 02:15:31 [INFO] router: Route selected: flux
2026-07-01 02:15:31 [INFO] main: Knowledge base loaded: flux1[dev]info.md
2026-07-01 02:15:33 [INFO] retry: API call succeeded on attempt 1
2026-07-01 02:15:33 [INFO] main: Response received. Output length: 312 chars

For portrait generation, FLUX.1 [dev] is the recommended choice...
```

---

## Known limitations / Next steps

- `verify_ssl_certs=False` is used for local development in Russia; production deployment should use the properly installed Mintsifry certificate
- Conversation history is not persisted between runs (stateless single-turn)
- Local inference (Ollama/vLLM) not yet integrated — cloud API only
- `flux.schnellinfo.md` knowledge base exists but routing for Schnell variant not yet implemented

---

## Stack

- **LLM:** GigaChat (Sber) via `gigachat==0.2.1`
- **Config:** `python-dotenv`
- **Error handling:** Custom retry with exponential backoff
- **Logging:** Python `logging` module with structured format

---

*Part of [github.com/LLIAlt/diffusion-prompt-engineering](https://github.com/LLIAlt/diffusion-prompt-engineering)*
