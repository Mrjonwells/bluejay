#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "🔁 Running SEO sync..."
python3 dev_sync_seo.py || echo "SEO sync skipped or failed."

echo "✅ Adding blog and index files..."
git add frontend/blogs/*.html || echo "Blog files not found."
git add frontend/blog.html || echo "blog.html not found."
git add sync_and_push.sh || true

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."
