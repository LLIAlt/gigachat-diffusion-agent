import time
import logging
from gigachat.exceptions import (
    RateLimitError,
    ServerError,
    GigaChatException,
)

logger = logging.getLogger(__name__)


def call_with_retry(generate_fn, max_retries: int = 3, backoff_base: float = 2.0):
    """
    Wraps any GigaChat API call with retry logic.

    generate_fn: a no-argument function that performs the actual API call
                 (wrap your call in a lambda when passing it in).
    max_retries: how many attempts before giving up.
    backoff_base: exponential backoff multiplier, used when the server
                  doesn't specify a retry_after value.
    """
    for attempt in range(max_retries):
        try:
            result = generate_fn()
            logger.info(f"API call succeeded on attemp {attempt + 1}")
            return result

        except RateLimitError as e:
            wait = getattr(e, "retry_after", None) or backoff_base**attempt
            logger.warning(
                f"[Attempt {attempt+1}/{max_retries}] Rate limit hit. Waiting {wait}s..."
            )
            time.sleep(wait)

        except ServerError as e:
            wait = backoff_base**attempt
            logger.warning(
                f"[Attempt {attempt+1}/{max_retries}] Server error: {e}. Retrying in {wait}s..."
            )
            time.sleep(wait)

        except GigaChatException as e:
            logger.error(f"GigaChat error (non-retryable): {e}")
            raise

    raise RuntimeError(f"Max retries ({max_retries}) exceeded.")
