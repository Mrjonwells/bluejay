import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INPUT_LOG = "backend/logs/interaction_log.jsonl"
OUTPUT_RECS = "backend/config/brain_update_recommendations.json"

if not os.path.exists(INPUT_LOG):
    print(f"Log file not found at {INPUT_LOG}. Skipping QA pass.")
    exit(0)

def load_interactions(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def generate_feedback(thread_id, assistant_msgs):
    if not assistant_msgs:
        return None
    recent = assistant_msgs[-3:] if len(assistant_msgs) >= 3 else assistant_msgs
    prompt = [
        {
            "role": "system",
            "content": "You are a senior sales copy editor reviewing AI assistant conversations. Find vague, repetitive, or low-conversion responses. Rewrite them to be shorter, sharper, and more persuasive — like a top human rep closing a sale."
        },
        {
            "role": "user",
            "content": "\n\n".join(recent)
        }
    ]
    try:
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            temperature=0.5
        )
        suggestion = result.choices[0].message.content.strip()
        return {"thread_id": thread_id, "improvement": suggestion}
    except Exception as e:
        print(f"Error analyzing thread {thread_id}: {e}")
        return None

def run_qa_challenger():
    logs = load_interactions(INPUT_LOG)
    recs = []
    for entry in logs:
        thread_id = entry.get("thread_id", "unknown")
        messages = entry.get("messages", [])
        assistant_replies = [m["content"] for m in messages if m["role"] == "assistant"]
        feedback = generate_feedback(thread_id, assistant_replies)
        if feedback:
            recs.append(feedback)
    os.makedirs(os.path.dirname(OUTPUT_RECS), exist_ok=True)
    with open(OUTPUT_RECS, "w") as f:
        json.dump(recs, f, indent=2)
    print(f"Generated {len(recs)} improvement recommendations.")

if __name__ == "__main__":
    run_qa_challenger()
