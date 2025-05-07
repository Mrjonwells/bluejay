import json
from collections import Counter
import re

LOG_PATH = "backend/logs/interaction_log.jsonl"

user_inputs = []

with open(LOG_PATH, "r") as f:
    for line in f:
        try:
            entry = json.loads(line)
            user_inputs.append(entry.get("user_input", "").lower())
        except:
            continue

# Extract tokens
tokens = []
for text in user_inputs:
    clean = re.sub(r"[^a-zA-Z0-9\s']", "", text)
    tokens.extend(clean.split())

# Show most common user words
common_words = Counter(tokens).most_common(30)

print("\n🔍 Top 30 Words from User Input:")
for word, count in common_words:
    print(f"{word}: {count}")
