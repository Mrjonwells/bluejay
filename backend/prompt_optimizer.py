# backend/prompt_optimizer.py

import json
from collections import Counter
import os

LOG_PATH = os.path.join("backend", "logs", "objection_log.jsonl")

def get_top_objections(n=5):
    """Parse log and return most frequent objection phrases"""
    if not os.path.exists(LOG_PATH):
        return []

    counter = Counter()

    with open(LOG_PATH, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                for msg in entry.get("messages", []):
                    if msg["role"] == "user":
                        text = msg["content"].lower()
                        if any(k in text for k in ["not interested", "too expensive", "already have", "maybe later"]):
                            counter[text] += 1
            except:
                continue

    return [phrase for phrase, _ in counter.most_common(n)]


def build_optimized_prompt(base_brain: dict, template: dict) -> str:
    """Returns enhanced system prompt using objection log"""
    objections = get_top_objections()

    objection_lines = "\n".join(f"- {o}" for o in objections) if objections else "None recently."

    prompt = (
        f"You are BlueJay, a persuasive sales assistant.\n\n"
        f"Use this brain:\n{json.dumps(base_brain)}\n\n"
        f"Template:\n{json.dumps(template)}\n\n"
        f"Top recent objections from users:\n{objection_lines}\n\n"
        "Address objections head-on, respond helpfully, and guide users back to savings and setup."
    )

    return prompt
