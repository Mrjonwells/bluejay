import os
from dotenv import load_dotenv
from bluejay.brainstem import parse_redis_threads, generate_recommendations, save_output

load_dotenv()

if __name__ == "__main__":
    counts = parse_redis_threads()
    recs = generate_recommendations(counts)
    save_output(counts, recs)
