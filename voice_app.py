from audio.stt import record_once, transcribe
from audio.tts import speak

from llm.sql_agent import generate_sql
from llm.answer_agent import generate_answer
from db.queries import run_select_query
from config.settings import SQL_LLM_CONFIG, ANSWER_LLM_CONFIG

from utils.formatter import format_transactions

from intent.router import detect_intent
from knowledge.policies import get_policy_answer


CURRENT_USER_ID = 1

def needs_database(text):
    keywords = ["balance", "transactions", "account", "spent", "deposit"]
    return any(k in text.lower() for k in keywords)

def main():
    print("Bank Voice Ai awake..")

    while True:
        record_once()

        user_text = transcribe()
        if not user_text:
            continue

        print("You: ", user_text)

        if needs_database(user_text):
            try:
                sql = generate_sql(user_text, SQL_LLM_CONFIG, CURRENT_USER_ID)
                print("SQL: ", sql)

                rows = run_select_query(sql)

                if not rows:
                    answer = "There are not transactions available yet."
                
                else:
                    db_context = "\n".join(str(rows) for row in rows)
                    answer = generate_answer(
                        user_text,
                        db_context,
                        ANSWER_LLM_CONFIG
                    )
                    # answer = format_transactions(rows)

            except Exception as e:
                answer = "Sorry, something went wrong while processing your request."

        else:
            answer = "Please Ask Clearly"

        print("AI: ", answer)

        speak(answer)
        # intent = detect_intent(user_text)
        # if intent == "BANK_DATA":
        #     try:
        #         sql = generate_sql(user_text, SQL_LLM_CONFIG, CURRENT_USER_ID)
        #         print("SQL: ", sql)

        #         rows = run_select_query(sql)

        #         if not rows:
        #             answer = "There are no transactions available Yet."

        #         else:
        #             answer = format_transactions(rows)
        #     except Exception as e:
        #         print("ERROR: ", e)
        #         answer = "Sorry, I could not fetch your bank details right now."

        # elif intent == "BANK POLICY":
        #     answer = get_policy_answer(user_text)

        # else:
        #     answer = (
        #         "I can help with your bank balance, recent transactions, "
        #         "or bank rules. Please ask a banking-related question."
        #     )
        # print("AI: ", answer)

        # speak(answer)

if __name__ == '__main__':
    main()