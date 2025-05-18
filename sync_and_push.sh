#!/bin/bash

echo "🔁 Running SEO sync..."
python3 dev_sync_seo.py || echo "SEO sync skipped or failed."

echo "✅ Adding blog and index files..."
git add frontend/blog.html frontend/blogs/*.html 2>/dev/null || echo "Blog files not found."

echo "🚀 Committing all updates..."
git config --global user.name "BlueJay"
git config --global user.email "info@askbluejay.ai"
git commit -am "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git checkout main 2>/dev/null
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push https://github_pat_...@github.com/Mrjonwells/bluejay.git main || echo "Push failed."
