#!/bin/bash

# Set Git identity
git config user.name "BlueJay Bot"
git config user.email "bot@askbluejay.ai"

# Ensure remote is set
git remote remove origin 2>/dev/null
git remote add origin https://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@github.com/Mrjonwells/bluejay.git

echo "✅ Adding blog and index files..."
git add frontend/blog.html
git add frontend/blogs/*.html || echo "Blog files not found."

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."
