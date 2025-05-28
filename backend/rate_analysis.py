# backend/rate_analysis.py

def parse_rate_request(request):
    # Dummy parser
    return {"volume": 10000, "transactions": 500}

def get_suggested_rate(volume, transactions):
    # Placeholder logic
    return 0.0215 if volume > 5000 else 0.025

def estimate_savings(current_rate, suggested_rate, volume):
    # Estimate savings in dollars
    return (current_rate - suggested_rate) * volume