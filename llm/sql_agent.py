import re
from config.prompts import SQL_SYSTEM_PROMPT
from llm.client import call_llm
from config.prompts import DB_SCHEMA

import re

def extract_select_sql(text):
    if not text:
        return None

    # Remove markdown
    text = text.replace("```sql", "").replace("```", "").strip()

    # Find first SELECT statement
    match = re.search(r"(select\s+.*)", text, re.IGNORECASE | re.DOTALL)
    if not match:
        return None

    sql = match.group(1).strip()

    forbidden = ["insert", "update", "delete", "drop", "alter", "truncate"]
    if any(word in sql.lower() for word in forbidden):
        return None

    return sql


def generate_sql(user_text, config, user_id):
    messages = [
        {"role" : "system", "content" : SQL_SYSTEM_PROMPT},
        {
            "role" : "user",
            "content" : f"""
{DB_SCHEMA}

user question:
{user_text}

Write ONLY the SQL query.

"""
        }
    ]

    sql = call_llm(messages, config)

    print("RAW LLM SQL OUTPUT >>>", repr(sql))  # keep while testing

    sql = extract_select_sql(sql)

    if not sql:
        raise ValueError("Unsafe SQL generated")
    
    sql = inject_user_filter(sql, user_id)
    sql = remove_llm_user_filters(sql)

    return sql

def inject_user_filter(sql, user_id):
    sql = sql.rstrip(";")

    # Ensure accounts join exists
    if "join accounts" not in sql.lower():
        sql = sql.replace(
            "from transactions",
            "from transactions t join accounts a on t.account_id = a.id"
        )

    # Split SQL safely
    order_by = ""
    limit = ""

    if " order by " in sql.lower():
        sql, order_by = re.split(r"order\s+by", sql, flags=re.IGNORECASE, maxsplit=1)
        order_by = " ORDER BY " + order_by

    if " limit " in order_by.lower():
        order_by, limit = re.split(r"limit", order_by, flags=re.IGNORECASE, maxsplit=1)
        limit = " LIMIT " + limit

    sql = sql.strip()
    sql += f" WHERE a.customer_id = {user_id}"

    return sql + order_by + limit


import re

def remove_llm_user_filters(sql):
    # Remove WHERE clauses that reference customers or customer_id
    sql = re.sub(
        r"where\s+.*?(order\s+by|limit|$)",
        r"\1",
        sql,
        flags=re.IGNORECASE | re.DOTALL
    )
    return sql.strip()


