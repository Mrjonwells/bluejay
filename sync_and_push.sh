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
git checkout main || git checkout -b main
git fetch origin main
git reset --hard origin/main || echo "Remote reset failed."

echo "🧼 Cleaning any local untracked files..."
git clean -fd

echo "✅ Adding blog and index files..."
git add frontend/blog.html frontend/blogs/*.html || echo "No blog files to add."
git diff --cached --quiet || git commit -m "Auto-sync SEO and blog updates from BlueJay"

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Blog sync complete."