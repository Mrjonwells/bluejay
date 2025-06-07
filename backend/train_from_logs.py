import json
import os
import urllib.parse
from datetime import datetime
from brainstem import parse_redis_threads, generate_recommendations, save_output

if __name__ == "__main__":
    counts = parse_redis_threads()
    recs = generate_recommendations(counts)
    save_output(counts, recs)
