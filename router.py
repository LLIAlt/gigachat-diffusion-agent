from gigachat import GigaChat
from dotenv import load_dotenv
from retry import call_with_retry
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

with open("prompts/router.md", encoding="utf-8") as f:
    ROUTER_PROMPT = f.read()


def get_route(user_input: str) -> str:
    logger.info(f"Routing input: '{user_input[:50]}...'")
    with GigaChat(
        credentials=os.getenv("GIGACHAT_CREDENTIALS"), verify_ssl_certs=False
    ) as client:
        response = call_with_retry(
            lambda: client.chat(
                {
                    "messages": [
                        {"role": "system", "content": ROUTER_PROMPT},
                        {"role": "user", "content": user_input},
                    ],
                    "temperature": 0.0,
                    "max_tokens": 10,
                }
            )
        )
    route = response.choices[0].message.content.strip().lower()
    logger.info(f"Route selected: {route}")
    return route
