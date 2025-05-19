#!/bin/bash

echo "🔁 Running SEO sync..."
python3 dev_sync_seo.py || echo "SEO sync skipped or failed."

echo "✅ Preparing Git config..."
git config user.email "bluejay@askbluejay.ai"
git config user.name "BlueJay Bot"

echo "🔄 Setting remote origin..."
git remote remove origin 2>/dev/null
git remote add origin https://$GITHUB_PAT@github.com/Mrjonwells/bluejay.git

echo "⏪ Resetting detached HEAD (if any)..."
git fetch origin main
git checkout main
git reset --hard origin/main

echo "🧼 Cleaning any local untracked files..."
git clean -fd

echo "✅ Adding blog and index files..."
ls -la frontend/blogs/
git add frontend/blog.html frontend/blogs/*.html || echo "Blog files not found."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Blog sync complete."

# Rotate topic (optional cleanup)
if [ -f backend/seo/seo_config.json ]; then
  echo "♻️ Rotating SEO topic..."
  python3 -c '
import json
p = "backend/seo/seo_config.json"
with open(p, "r") as f: data = json.load(f)
if data.get("keywords"): data["keywords"] = data["keywords"][1:] + data["keywords"][:1]
with open(p, "w") as f: json.dump(data, f, indent=2)
print("Next topic:", data["keywords"][0])
' || echo "Keyword rotation failed."
fi