import asyncio
import traceback
from src.shared.utils.logger import logging
from src.shared.redis.redis import RedisKeys

def retry(redis_client, max_retries=5, delay=60):
    def decorator(func):
        async def wrapper(metric_generator, metric_title, llm_name, *args, **kwargs):
            retry_key = f"{RedisKeys.RETRY_BENCHMARKS.value}:{llm_name}:{metric_title}"

            current_attempt = redis_client.redis.get(retry_key)
            if current_attempt is None:
                current_attempt = 0
            else:
                current_attempt = int(current_attempt)

            while current_attempt <= max_retries:
                try:
                    return await func(metric_generator, metric_title, llm_name, *args, **kwargs)
                except Exception as e:
                    redis_client.redis.set(retry_key, current_attempt + 1, ex=60)
                    traceback.print_exc()
                    logging.error(f"Error generating metrics for LLM {llm_name}, attempt {current_attempt + 1}: {str(e)}")

                    current_attempt += 1
                    if current_attempt <= max_retries:
                        await asyncio.sleep(delay)

            logging.info(f"Maximum retries reached for LLM {llm_name} : metric {metric_title}!")
            return None

        return wrapper

    return decorator
