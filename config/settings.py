import os
from dotenv import load_dotenv


load_dotenv()
LLM_URL = os.getenv("LLM_URL")
LLM_MODEL = "phi-3-mini-instruct"

SQL_LLM_CONFIG = {
    "temperatue" : 0,
    "max_tokens" : 150,
    "top_p" : 1
}

ANSWER_LLM_CONFIG = {
    "temperature" : 0.3,
    "max_tokens" : 200
}