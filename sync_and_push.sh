#!/bin/bash

echo "🔁 Running SEO sync..."
python3 dev_sync_seo.py || echo "SEO sync skipped or failed."

echo "✅ Adding blog and index files..."
git config user.email "bluejay@askbluejay.ai"
git config user.name "BlueJay Bot"

git add frontend/blog.html frontend/blogs/*.html || echo "Blog files not found."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push https://$GITHUB_PAT@github.com/Mrjonwells/bluejay.git || echo "Push failed."
