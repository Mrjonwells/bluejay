#!/bin/bash

echo "🔁 Running SEO sync..."
python3 backend/generators/dev_sync_seo.py

echo "✅ Pulling latest from GitHub to avoid push rejection..."
git fetch origin main
git reset --hard origin/main

echo "✅ Committing SEO updates..."
git add frontend/index.html backend/seo/seo_config.json

echo "📝 Adding new blog posts..."
git add frontend/blogs/*.html frontend/blog.html

echo "🚀 Committing all updates..."
git config --global user.name "BlueJay"
git config --global user.email "info@askbluejay.ai"
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "No changes to commit"

echo "🔼 Pushing to GitHub..."
git push https://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@github.com/Mrjonwells/bluejay.git main
