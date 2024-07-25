# test_api.py
import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("TUNEAI_API_KEY")


def test_api_call():
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json",
    }
    data = {
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": "You are a creative story writer."},
            {"role": "user", "content": "Write a short story about a mischievous robot in a library."}
        ],
        "model": "meta/llama-3.1-405b-instruct",
        "stream": False,
        "frequency_penalty": 0,
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")


if __name__ == "__main__":
    test_api_call()