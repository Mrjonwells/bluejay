import os
import json
from openai import OpenAI

# Load environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

INPUT_LOG = "backend/logs/objection_log.jsonl"
OUTPUT_RECS = "brain_update_recommendations.json"

def load_objection_logs(path):
    if not os.path.exists(path):
        print(f"No objection log found at {path}.")
        return []
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def extract_objection_threads(logs):
    results = []
    for entry in logs:
        messages = entry.get("messages", [])
        for i, msg in enumerate(messages):
            if msg["role"] == "user":
                text = msg["content"].lower()
                if any(kw in text for kw in ["not interested", "already have", "too expensive", "let me think", "busy right now"]):
                    assistant_reply = ""
                    for j in range(i+1, len(messages)):
                        if messages[j]["role"] == "assistant":
                            assistant_reply = messages[j]["content"]
                            break
                    results.append((text, assistant_reply))
                    break
    return results

def improve_response(objection, reply):
    prompt = [
        {"role": "system", "content": "You are a persuasive sales strategist improving how an AI handles objections. The user expressed: '" + objection + "'. Here is the AI’s current reply:\n" + reply + "\n\nImprove it to sound more human, respectful, and confident. Respond like a great rep who keeps the conversation going."},
        {"role": "user", "content": "Rewrite the assistant's reply to be more persuasive."}
    ]
    try:
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt,
            temperature=0.6
        )
        suggestion = result.choices[0].message.content.strip()
        return {"type": "objection_update", "trigger": objection, "improvement": suggestion}
    except Exception as e:
        print(f"Error improving objection '{objection}': {e}")
        return None

def run_objection_trainer():
    logs = load_objection_logs(INPUT_LOG)
    threads = extract_objection_threads(logs)
    recs = []

    for objection, reply in threads:
        improved = improve_response(objection, reply)
        if improved:
            recs.append(improved)

    with open(OUTPUT_RECS, "a") as f:
        for rec in recs:
            f.write(json.dumps(rec) + "\n")
    print(f"Generated {len(recs)} objection improvements.")

if __name__ == "__main__":
    run_objection_trainer()
