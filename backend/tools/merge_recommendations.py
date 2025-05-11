import json
import os
from datetime import datetime

RECOMMENDATIONS_PATH = "backend/config/brain_update_recommendations.json"
BRAIN_PATH = "backend/config/bluejay_config.json"
OUTPUT_LOG = "backend/logs/brain_update_log.jsonl"

# Simple logic to apply recommendations to the brain
def merge_changes(brain, recs):
    if not recs:
        return brain

    for rec in recs:
        if "monthly_card_volume" in rec:
            brain["follow_up_styles"]["assertive"] = "Want to lock in your monthly volume savings?"
        if "average_ticket" in rec:
            brain["follow_prompts"].insert(1, "What’s your average ticket size typically?")
        if "processor" in rec:
            brain["objections"]["already have a system"] = "You mentioned a processor — want to compare it with ours?"
        if "transaction_type" in rec:
            brain["product_recommendations"]["online"]["reply"] += " We also support full tap-to-pay setups."
        if "business_name" in rec:
            brain["personality"]["ego_bump"] = "Sounds like a legit operation — respect."
        if "contact_info" in rec:
            brain["follow_prompts"].append("Mind sharing your email or best phone to follow up?")

    return brain

def main():
    if not os.path.exists(RECOMMENDATIONS_PATH):
        print("No update recommendations found.")
        return

    with open(RECOMMENDATIONS_PATH, "r") as f:
        rec_data = json.load(f)

    recs = rec_data.get("recommendations", [])
    if not recs:
        print("No recommendations to apply.")
        return

    if not os.path.exists(BRAIN_PATH):
        print("No brain config found.")
        return

    with open(BRAIN_PATH, "r") as f:
        brain = json.load(f)

    updated_brain = merge_changes(brain, recs)

    with open(BRAIN_PATH, "w") as f:
        json.dump(updated_brain, f, indent=2)

    # Log the update
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)
    with open(OUTPUT_LOG, "a") as log:
        log.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "applied_recommendations": recs
        }) + "\n")

    print("Brain config updated based on recommendations.")

if __name__ == "__main__":
    main()
