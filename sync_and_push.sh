#!/bin/bash

# Set identity permanently (safe across runs)
git config --global user.name "BlueJay Bot"
git config --global user.email "bluejay@askbluejay.ai"

# Ensure remote is configured once
git remote get-url origin > /dev/null 2>&1
if [ $? -ne 0 ]; then
  git remote add origin https://Mrjonwells:${BLUEJAY_PAT}@github.com/Mrjonwells/bluejay.git
fi

# Add and commit updates
echo "✅ Adding blog and index files..."
git add frontend/blogs/*.html frontend/blog.html

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Sync complete."
