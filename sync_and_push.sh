#!/bin/bash
echo "==> Running blog and SEO sync..."

# Set up Git identity
git config user.name "BlueJay Bot"
git config user.email "ask@askbluejay.ai"

# Checkout main branch
git checkout main || git checkout -b main

# Clean up
echo "🧼 Cleaning any local untracked files..."
git reset --hard
git clean -fd

# Add changes
echo "✅ Adding blog and index files..."
git add frontend/blog.html frontend/blogs/*.html 2>/dev/null || echo "No blog posts found to add."

# Commit if needed
if ! git diff --cached --quiet; then
  echo "🚀 Committing all updates..."
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
else
  echo "Nothing to commit."
fi

# Pull before push
echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase --autostash || git rebase --skip || echo "Pull failed (non-blocking)."

# Push
echo "🔼 Pushing to GitHub..."
git push https://github_pat_***REDACTED***@github.com/Mrjonwells/bluejay.git main || echo "Push failed."

echo "✅ Sync complete."

# Rotate SEO keyword (if applicable)
if [ -f backend/seo/seo_config.json ]; then
  echo "♻️ Rotating SEO topic..."
  python3 backend/seo/rotate_keyword.py
fi
