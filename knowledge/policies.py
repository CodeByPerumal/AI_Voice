BANK_POLICIES = {
    "withdrawal": "You can withdraw up to 50,000 rupees per day.",
    "interest": "Savings accounts earn 3.5 percent annual interest.",
    "charges": "No charges are applied for standard transactions."
}


def get_policy_answer(text):
    text = text.lower()

    if "withdraw" in text:
        return BANK_POLICIES["withdrawal"]

    if "interest" in text:
        return BANK_POLICIES["interest"]

    if "charge" in text or "fee" in text:
        return BANK_POLICIES["charges"]

    return "Please contact the bank for detailed policy information."