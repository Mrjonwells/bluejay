import os

def get_all_metrics():
    """
    Returns a dictionary of usage and cost metrics for core services.
    Replace static values with API calls if needed.
    """
    return {
        "OpenAI": {
            "cost": float(os.getenv("OPENAI_SPEND", "12.45")),
            "limit": float(os.getenv("OPENAI_LIMIT", "50"))
        },
        "Render": {
            "cost": float(os.getenv("RENDER_SPEND", "7.30")),
            "limit": float(os.getenv("RENDER_LIMIT", "25"))
        },
        "GitHub": {
            "cost": float(os.getenv("GITHUB_SPEND", "0.0")),
            "limit": float(os.getenv("GITHUB_LIMIT", "5"))
        }
    }

def update_brain_config(param, value):
    """
    Central update logic for config parameters.
    Add write-back to config or database here if needed.
    """
    # Simulated response - extend this as needed
    return f"🔁 Updated `{param}` to `{value}`"

def undo_last_change():
    """
    Placeholder for undo functionality — to be implemented.
    """
    return "↩️ Undo not yet implemented."
