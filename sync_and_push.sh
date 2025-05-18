#!/bin/bash

echo "🔁 Running SEO sync..."
python dev_sync_seo.py

echo "✅ Committing SEO updates..."
git add frontend/index.html backend/seo/seo_config.json

echo "📝 Adding new blog posts..."
git add frontend/blogs/*.html frontend/blog.html || true

echo "🚀 Committing all updates..."
git config user.email "info@askbluejay.ai"
git config user.name "BlueJay"
git commit -m "Auto-sync SEO and blog updates from BlueJay" || true

echo "🔼 Pushing to GitHub..."
git remote add origin https://github.com/Mrjonwells/bluejay.git 2>/dev/null || true
git push origin main
