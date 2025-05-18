#!/bin/bash

echo "🔁 Running SEO sync..."
cd backend/generators || exit
python3 ../../dev_sync_seo.py || echo "SEO sync skipped or failed."
cd ../../

echo "✅ Adding blog and index files..."
git add frontend/blog.html frontend/blogs/*.html 2>/dev/null || echo "Blog files not found."

echo "🚀 Committing all updates..."
git config --global user.name "BlueJay"
git config --global user.email "info@askbluejay.ai"
git commit -am "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git checkout main 2>/dev/null
git pull https://github.com/Mrjonwells/bluejay.git main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push https://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@github.com/Mrjonwells/bluejay.git main || echo "Push failed."
