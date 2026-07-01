from gigachat import GigaChat
from router import get_route
from dotenv import load_dotenv
from retry import call_with_retry
import logging
import os

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

with open("prompts/DMassistant.md", "r", encoding="utf-8") as file:
    assistant_prompt = file.read()

user_input = input("> ")
route = get_route(user_input)
knowledge = ""
if route == "flux":
    with open("knowledge/flux1[dev]info.md", encoding="utf-8") as file:
        knowledge = file.read()
    logger.info("Knowledge base loaded: flux1[dev]info.md")
elif route == "qwen":
    with open("knowledge/qwen-imageinfo.md", encoding="utf-8") as file:
        knowledge = file.read()
    logger.info("Knowledge base loaded: qwen-imageinfo.md")
else:
    logger.warning(f"Unknown route '{route}' - proceeding without knowledge base")

system_prompt = assistant_prompt + "\n\n" + knowledge

with GigaChat(
    credentials=os.getenv("GIGACHAT_CREDENTIALS"), verify_ssl_certs=False
) as client:
    response = call_with_retry(
        lambda: client.chat(
            {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input},
                ],
                "temperature": 0.7,
                "max_tokens": 800,
            }
        )
    )


result = response.choices[0].message.content
logger.info(f"Response received. Output length: {len(result)} chars")
print(result)
