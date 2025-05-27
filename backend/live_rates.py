# backend/live_rates.py

DEFAULT_PLATFORM_RATES = {
    "square": 2.6,
    "paypal": 2.9,
    "stripe": 2.9,
    "clover": 2.7,
    "shopify": 2.7,
    "toast": 2.5
}


def parse_rate_request(user_input: str) -> dict:
    """Extracts rate and platform if mentioned by user"""
    text = user_input.lower()
    platform = None
    rate = None

    for name in DEFAULT_PLATFORM_RATES:
        if name in text:
            platform = name
            break

    # look for % or decimal rate
    for token in text.replace("%", "").split():
        try:
            val = float(token)
            if 0 < val < 100:
                rate = val
                break
        except:
            continue

    return {"platform": platform, "rate": rate}


def estimate_savings(user_rate: float, bluejay_rate: float = 2.1, volume_monthly: float = 10000.0) -> float:
    """
    Estimate monthly savings based on user's current rate.
    Default BlueJay rate = 2.1%, default volume = $10,000
    """
    delta = user_rate - bluejay_rate
    if delta <= 0:
        return 0.0
    return round((delta / 100) * volume_monthly, 2)


def get_suggested_rate(platform: str) -> float:
    """Return most common rate for a known platform"""
    return DEFAULT_PLATFORM_RATES.get(platform.lower())
