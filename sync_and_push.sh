#!/bin/bash

echo "🔁 Running SEO sync..."
python dev_sync_seo.py

echo "✅ Committing SEO updates..."
git add frontend/index.html backend/seo/seo_config.json

echo "📝 Adding new blog posts..."
git add frontend/blogs/*.html frontend/blog.html

echo "🚀 Committing all updates..."
git config user.email "info@askbluejay.ai"
git config user.name "BlueJay"
git commit -m "Auto-sync SEO and blog updates from BlueJay"

echo "🔼 Pushing to GitHub..."
git remote set-url origin https://Mrjonwells:${GITHUB_PAT}@github.com/Mrjonwells/bluejay.git
git push origin main
