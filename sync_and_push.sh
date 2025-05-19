# Ensure you're in repo root
cd "$(dirname "$0")"

# Ensure Git is on main
git checkout main || git checkout -b main

# Add blog files properly from the repo root
git add frontend/blogs/*.html frontend/blog.html || echo "No blog files to add"

# Commit if anything is staged
git diff --cached --quiet || git commit -m "Auto-sync SEO and blog updates from BlueJay"

# Pull latest before pushing (fast-forward safe)
git pull origin main --rebase || echo "Pull failed (non-blocking)"

# Push safely
git push origin main || echo "Push failed"

echo "✅ Sync complete."
