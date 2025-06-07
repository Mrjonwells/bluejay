from flask import Blueprint, request, jsonify
import openai
import os
from datetime import datetime
bp = Blueprint("brain_edit", __name__)
# Backup path before edits
BACKUP_DIR = "backend/backups"
os.makedirs(BACKUP_DIR, exist_ok=True)
# Files affected by brainstem edits
DEPENDENT_FILES = [
"backend/brainstem.py",
"backend/train_from_logs.py",
"backend/generate_training_report.py"
]
@bp.route("/api/brain_edit", methods=["POST"])
def edit_brain():
data = request.get_json()
instruction = data.get("instruction", "")
if not instruction:
return jsonify({"error": "Missing instruction"}), 400
# Backup all files
timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
for path in DEPENDENT_FILES:
with open(path, "r") as f:
content = f.read()
backup_path = os.path.join(BACKUP_DIR,
f"{Path(path).stem}_{timestamp}.bak")
with open(backup_path, "w") as f:
f.write(content)
# Call OpenAI to get updated code
openai.api_key = os.getenv("OPENAI_API_KEY")
messages = [
{"role": "system", "content": "You are BlueJayâs
centralized AI editor. Update brainstem.py and propagate updates
to linked files. Only change relevant parts."},
{"role": "user", "content": instruction}
]
completion = openai.ChatCompletion.create(
model="gpt-4",
messages=messages,
temperature=0.2
)
response = completion.choices[0].message.content
# You could parse changes or write full file edits here
# For now, just return the suggestion to frontend
return jsonify({"response": response})
