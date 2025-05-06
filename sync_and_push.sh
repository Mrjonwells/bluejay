#!/bin/bash
echo "🔁 Running SEO sync..."
python dev_sync_seo.py

echo "✅ Committing SEO updates..."
git add frontend/index.html backend/seo/seo_config.json
git commit -m "Auto-sync SEO from Google Trends"
git push
