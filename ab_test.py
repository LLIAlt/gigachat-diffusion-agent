from dotenv import load_dotenv
from gigachat import GigaChat
from retry import call_with_retry
import os
import logging

load_dotenv()
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


TEST_CASES = [
    {"input": "I wanna generate image of old man", "expected": "flux"},
    {"input": "How to set up FLUX for portrait generation?", "expected": "flux"},
    {"input": "What sampler should I use in FLUX?", "expected": "flux"},
    {"input": "Which model is better for anime style?", "expected": "qwen"},
    {"input": "How does Qwen handle image prompts?", "expected": "qwen"},
    {"input": "I want to generate a landscape photo", "expected": "flux"},
    {"input": "Tell me about Qwen image parameters", "expected": "qwen"},
    {"input": "Best settings for photorealistic output", "expected": "flux"},
]


def run_test(prompt_text: str, label: str) -> dict:
    correct = 0
    results = []

    with GigaChat(
        credentials=os.getenv("GIGACHAT_CREDENTIALS"), verify_ssl_certs=False
    ) as client:
        for case in TEST_CASES:
            response = call_with_retry(
                lambda: client.chat(
                    {
                        "messages": [
                            {"role": "system", "content": prompt_text},
                            {"role": "user", "content": case["input"]},
                        ],
                        "temperature": 0.0,
                        "max_tokens": 10,
                    }
                )
            )

            got = response.choices[0].message.content.strip().lower()
            is_correct = got == case["expected"]
            if is_correct:
                correct += 1

            results.append(
                {
                    "input": case["input"],
                    "expected": case["expected"],
                    "got": got,
                    "correct": is_correct,
                }
            )

    accuracy = correct / len(TEST_CASES)
    logger.info(f"[{label}] Accuracy: {accuracy:.0%} ({correct}/{len(TEST_CASES)})")
    return {"label": label, "accuracy": accuracy, "results": results}


def print_report(result: dict):
    print(f"\n=== {result['label']} — {result['accuracy']:.0%} ===")
    for r in result["results"]:
        status = "✅" if r["correct"] else "❌"
        print(
            f"{status} Expected: {r['expected']:6} | Got: {r['got']:6} | {r['input'][:45]}"
        )


with open("prompts/router.md", encoding="utf-8") as f:
    prompt_a = f.read()

with open("prompts/router_b.md", encoding="utf-8") as f:
    prompt_b = f.read()

## TEST of md
logger.info("Starting A/B test...")
result_a = run_test(prompt_a, "Prompt A (original)")
result_b = run_test(prompt_b, "Prompt B (variant)")

print_report(result_a)
print_report(result_b)

# WINNER TAKES IT ALL
print("\n=== WINNER ===")
if result_b["accuracy"] > result_a["accuracy"]:
    print(f"Prompt B wins: {result_b['accuracy']:.0%} vs {result_a['accuracy']:.0%}")
elif result_a["accuracy"] > result_b["accuracy"]:
    print(f"Prompt A wins: {result_a['accuracy']:.0%} vs {result_b['accuracy']:.0%}")
else:
    print(f"Tie: both scored {result_a['accuracy']:.0%}")
