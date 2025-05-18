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
git commit -m "Auto-sync SEO and blog updates" || echo "Nothing to commit."

echo "🔼 Pushing to GitHub..."
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git 2>/dev/null || true
git push origin main
