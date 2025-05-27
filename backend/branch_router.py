# backend/branch_router.py

def detect_intent(user_input: str) -> str:
    text = user_input.lower()

    if any(kw in text for kw in ["rates", "pricing", "fees", "interchange"]):
        return "pricing_info"

    if any(kw in text for kw in ["how do i start", "setup", "get started", "signup"]):
        return "onboarding"

    if any(kw in text for kw in ["not interested", "too expensive", "maybe later", "already have"]):
        return "objection"

    if any(kw in text for kw in ["calculate", "savings", "save money", "compare"]):
        return "savings_calc"

    if any(kw in text for kw in ["pos", "terminal", "device", "integration", "api"]):
        return "technical_question"

    if any(kw in text for kw in ["hello", "hi", "good morning", "evening"]):
        return "greeting"

    return "general_inquiry"
