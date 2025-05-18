#!/bin/bash

echo "🔁 Running SEO sync..."
python dev_sync_seo.py

echo "✅ Committing SEO updates..."
git add frontend/index.html backend/seo/seo_config.json

echo "📝 Adding new blog posts..."
git add frontend/blogs/*.html frontend/blog.html

echo "🚀 Committing all updates..."
git config --global user.name "BlueJay"
git config --global user.email "info@askbluejay.ai"
git commit -m "Auto-sync SEO and blog updates from BlueJay"

echo "🔼 Pushing to GitHub..."
git push https://<YOUR_GITHUB_PAT>@github.com/Mrjonwells/bluejay.git main
