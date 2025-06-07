import os

def get_all_metrics():
    """Returns mock spend/limit data. Replace with real usage if needed."""
    return {
        "OpenAI": {
            "cost": float(os.getenv("OPENAI_SPEND", 0)),
            "limit": float(os.getenv("OPENAI_LIMIT", 50))
        },
        "Render": {
            "cost": float(os.getenv("RENDER_SPEND", 0)),
            "limit": float(os.getenv("RENDER_LIMIT", 25))
        },
        "GitHub": {
            "cost": float(os.getenv("GITHUB_SPEND", 0)),
            "limit": float(os.getenv("GITHUB_LIMIT", 5))
        }
    }

def get_brain_code():
    """Loads brainstem.py contents as editable text."""
    try:
        with open(__file__, "r") as f:
            return f.read()
    except Exception as e:
        return f"# Failed to load brain: {e}"

def save_brain_code(new_code: str):
    """Saves new content into brainstem.py."""
    path = __file__
    with open(path, "w") as f:
        f.write(new_code)
