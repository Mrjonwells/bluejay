#!/bin/bash

cd "$(dirname "$0")"

# Set git identity
git config --global user.email "bluejay@askbluejay.ai"
git config --global user.name "BlueJay Bot"

# Run generator
python3 backend/generators/blog_generator_runner.py

# Stage and commit changes
git add frontend/blogs/ frontend/blog.html || true
git diff --cached --quiet || git commit -m "Auto-sync SEO and blog updates from BlueJay"

# Push to GitHub
git push https://x-access-token:${BLUEJAY_PAT}@github.com/Mrjonwells/bluejay.git
