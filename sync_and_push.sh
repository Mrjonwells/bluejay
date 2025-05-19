#!/bin/bash

# Set Git user identity
git config --global user.email "auto@askbluejay.ai"
git config --global user.name "BlueJay AutoBot"

# Move to project root (assumes this script runs from /opt/render/project/src/)
cd "$(dirname "$0")"

# Add blog files explicitly
git add frontend/blog.html
git add frontend/blogs/*.html

# Commit changes if any
git diff --cached --quiet || git commit -m "Auto-sync SEO and blog updates from BlueJay"

# Pull latest from GitHub main before pushing
git pull origin main --rebase || echo "Pull failed (non-blocking)."

# Push to GitHub using token
git push https://$GITHUB_PAT@github.com/Mrjonwells/bluejay.git main || echo "Push failed."
