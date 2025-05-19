#!/bin/bash
set -e

echo "📂 Switching to main branch..."
git checkout main || git checkout -b main

echo "🔄 Pulling latest from GitHub..."
git pull --rebase --autostash origin main || echo "Non-blocking pull failure."

echo "🧼 Cleaning any local untracked files..."
rm -f frontend/blogs/.txt || true

echo "✅ Adding blog and index files..."
ls -l frontend/blogs || echo "No blogs directory yet"

# Ensure frontend/blog.html and all blog posts are tracked
git add frontend/blog.html || echo "No index file found."
git add frontend/blogs/*.html || echo "No blog posts found to add."

echo "🚀 Committing all updates..."
git config --global user.email "ask@askbluejay.ai"
git config --global user.name "BlueJay Bot"
git commit -am "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "🔁 Running SEO sync..."
python3 backend/dev_sync_seo.py || echo "SEO sync skipped or failed."

echo "✅ Blog sync complete."
