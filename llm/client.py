import requests
from config.settings import LLM_URL, LLM_MODEL


def call_llm(messages, config):
    payload = {
        "model" : LLM_MODEL,
        "messages" : messages,
        "temperature" : config.get("temperature", 0),
        "max_tokens" : config.get("max_tokens", 256),
        "top_p" : config.get("top_p", 1)
    }
    response = requests.post(LLM_URL, json = payload)
    response.raise_for_status()
    # print("LLM PAYLOAD:", payload)

    return response.json()["choices"][0]["message"]["content"].strip()