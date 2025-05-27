# backend/lead_scoring.py

def score_lead(volume: float, transactions: int) -> int:
    """
    Scores a lead from 0–100 based on monthly volume and transaction count.
    """
    vol_score = min(int((volume or 0) / 1000 * 10), 50)  # up to 50 pts
    tx_score = min(int((transactions or 0) / 100 * 5), 50)  # up to 50 pts
    return vol_score + tx_score


def parse_lead_details(user_input: str) -> dict:
    """
    Attempts to extract monthly volume and estimated transactions from user input.
    Looks for keywords like 'volume', 'transactions', 'per month', etc.
    """
    text = user_input.lower()
    volume = 0
    transactions = 0

    for word in text.replace("$", "").replace(",", "").split():
        try:
            num = float(word)
            if "transaction" in text or "swipe" in text or "sales" in text:
                if 10 <= num <= 100000:
                    transactions = int(num)
            elif "volume" in text or "month" in text or "process" in text:
                if num > 500:
                    volume = float(num)
        except:
            continue

    return {"volume": volume, "transactions": transactions}
