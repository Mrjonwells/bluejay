#!/bin/bash
set -e

echo "🔁 Syncing blog content..."

# Ensure we're at the repo root
cd "$(dirname "$0")"

# Set Git identity (Render doesn't do this by default)
git config user.name "BlueJay Bot"
git config user.email "bot@askbluejay.ai"

# Ensure 'origin' is set
git remote remove origin 2>/dev/null || true
git remote add origin https://$GITHUB_PAT@github.com/Mrjonwells/bluejay.git

# SEO sync first
echo "🔁 Running SEO sync..."
if [ -f backend/dev_sync_seo.py ]; then
  python3 backend/dev_sync_seo.py || echo "SEO sync skipped or failed."
else
  echo "SEO script not found, skipping."
fi

# Stage all generated blog files and blog index
echo "✅ Adding blog and index files..."
git add frontend/blog.html || echo "No index file found."
git add frontend/blogs/*.html || echo "No blog posts found to add."

# Commit changes if any
if git diff --cached --quiet; then
  echo "Nothing to commit."
else
  echo "🚀 Committing all updates..."
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
fi

# Pull latest (non-blocking)
echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

# Push to GitHub
echo "🔼 Pushing to GitHub..."
git push origin HEAD:main || echo "Push failed."

echo "✅ Sync complete."
