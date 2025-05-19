#!/bin/bash

# Set Git identity for Render environment
git config --global user.name "BlueJay Bot"
git config --global user.email "bot@askbluejay.ai"

echo "✅ Adding blog and index files..."

cd "$(dirname "$0")/.." || exit

# Stage blog files
find frontend/blogs/ -name "*.html" -exec git add {} +
git add frontend/blog.html || true

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Sync complete."
