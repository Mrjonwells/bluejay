#!/bin/bash

# Set Git identity
git config --global user.name "BlueJay Bot"
git config --global user.email "bluejay@askbluejay.ai"

echo "✅ Adding blog and index files..."
find frontend/blogs/ -type f -name "*.html" -exec git add {} \;
git add frontend/blog.html || true

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || true

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || true

echo "🔼 Pushing to GitHub..."
git push origin main || true

echo "✅ Sync complete."
