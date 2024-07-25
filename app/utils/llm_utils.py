import requests
import logging
from app.config import API_KEY

logger = logging.getLogger(__name__)


def get_llm_response(messages, temperature=0.7, max_tokens=2048, stream=False):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "temperature": temperature,
        "messages": messages,
        "model": "meta/llama-3.1-405b-instruct",
        "stream": stream,
        "frequency_penalty": 0,
        "max_tokens": max_tokens
    }

    logger.debug(f"Sending request to {url} with data: {data}")

    response = requests.post(url, headers=headers, json=data)

    logger.debug(f"Received response with status code: {response.status_code}")
    logger.debug(f"Response content: {response.text[:500]}...")  # Log first 500 characters

    response.raise_for_status()

    if stream:
        return response.iter_lines()
    else:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()