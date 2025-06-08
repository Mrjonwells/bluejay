import json
import os
import sys
import urllib.parse
from datetime import datetime

# Ensure local import works on Render cron
sys.path.append(os.path.dirname(__file__))

from brainstem import parse_redis_threads, generate_recommendations, save_output

if __name__ == "__main__":
    counts = parse_redis_threads()
    recs = generate_recommendations(counts)
    save_output(counts, recs)
