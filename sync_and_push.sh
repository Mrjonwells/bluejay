#!/bin/bash

echo "🔁 Running SEO sync..."
cd backend || exit 1
python3 dev_sync_seo.py || echo "SEO sync skipped or failed."
cd ..

echo "✅ Staging blog files..."
git add frontend/blog.html frontend/blogs/*.html 2>/dev/null || echo "Blog files not found."

echo "🚀 Committing updates..."
git config --global user.name "BlueJay"
git config --global user.email "info@askbluejay.ai"
git commit -am "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub main..."
git checkout main 2>/dev/null
git pull origin main --rebase || echo "Pull failed — continuing anyway."

echo "🔼 Pushing to GitHub..."
git push https://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@github.com/Mrjonwells/bluejay.git main || echo "Push failed."
