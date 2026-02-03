from db.mysql import get_db

def run_select_query(sql):
    conn = get_db()
    cursor = conn.cursor(dictionary = True)
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# Note : INSERT, UPDATE, DELETE, DROP [ Not Possible ]
# Only SELECT is allowed.