def detect_intent(text : str) -> str:
    text = text.lower()

    bank_data_keywords = [
        "transaction", "transactions", "balance", "spent",
        "deposit", "withdraw", "account"
    ]

    bank_policy_keywords = [
        "policy", "rule", "rules", "limit",
        "interest", "charges", "fees"
    ]

    if any(k in text for k in bank_data_keywords):
        return "BANK_DATA"
    
    if any(k in text for k in bank_policy_keywords):
        return "BANK_POLICY"
    
    return "GENERAL"