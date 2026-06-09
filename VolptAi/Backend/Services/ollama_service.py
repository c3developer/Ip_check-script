import requests

from config import (
    OLLAMA_URL,
    MODEL_NAME
)


def ask_ai(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"]