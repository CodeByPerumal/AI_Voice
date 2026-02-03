from datetime import datetime

def format_transactions(rows):
    if not rows:
        return "There are not transactions available Yet."
    
    sentences = []

    for i, row in enumerate(rows, start=1):
        amount = row["amount"]
        txn_type = row["type"]
        date = row["created_at"]

        if isinstance(date, datetime):
            date_str = date.strftime("%B %d at %I:%M:%p")
        else:
            date_str = str(date)

        sentence = (
            f"Transaction {i}: "
            f"a {txn_type} of {amount} rupees on {date_str}."
        )

        sentences.append(sentence)

    return " ".join(sentences)