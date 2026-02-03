from config.prompts import ANSWER_SYSTEM_PROMPT
from llm.client import call_llm

def generate_answer(user_text, db_context, config):
    messages = [
        {
            "role" : "system",
            "content" : ANSWER_SYSTEM_PROMPT
        },
        {
            "role" : "assistant",
            "content" : db_context
        },
        {
            "role" : "user",
            "content" : user_text
        }
    ]

    return call_llm(messages, config)