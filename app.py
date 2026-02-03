from llm.sql_agent import generate_sql
from llm.answer_agent import generate_answer
from db.queries import run_select_query
from config.settings import SQL_LLM_CONFIG, ANSWER_LLM_CONFIG

CURRENT_USER_ID = 1

def needs_database(text):
    keywords = ["balance", "transactions", "account", "spent", "deposit"]
    return any(k in text.lower() for k in keywords)

def main():
    print("AI Assistant Ready (type 'exit' to quit)")


    while True:
        user_text = input("\nYou: ")

        if user_text.lower == "exit":
            break

        if needs_database(user_text):
            try:
                sql = generate_sql(user_text, SQL_LLM_CONFIG, CURRENT_USER_ID)
                print("SQL:", sql)

                rows = run_select_query(sql)

                if not rows:
                    db_context = "EMPTY_RESULT"
                else:
                    db_context = "\n".join(str(row) for row in rows)


                answer = generate_answer(
                    user_text,
                    db_context,
                    ANSWER_LLM_CONFIG
                )
            except Exception as e:
                answer = f"Error {str(e)}"
        else:
            answer = "This question does not require DB access"
        print("AI: ", answer)

if __name__ == '__main__':
    main()