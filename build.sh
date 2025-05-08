#!/bin/bash

echo "Starting SEO injection..."

# Wait briefly for Render to finish file syncing
sleep 2

# Run the SEO injector
python3 dev_sync_seo.py

echo "Finished SEO injection."
