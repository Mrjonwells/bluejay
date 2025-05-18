#!/bin/bash

# Set Git identity
git config --global user.name "BlueJay Bot"
git config --global user.email "bot@askbluejay.ai"

# Set GitHub remote
git remote remove origin 2>/dev/null
git remote add origin https://<YOUR_PAT>@github.com/Mrjonwells/bluejay.git

echo "✅ Adding blog and index files..."
git add frontend/blogs/*.html frontend/blog.html || echo "Blog files not found."

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."
