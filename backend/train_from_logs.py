# backend/train_from_logs.py

from brainstem import parse_redis_threads, generate_recommendations, save_output

if __name__ == "__main__":
    threads = parse_redis_threads()
    recs = generate_recommendations(threads)
    save_output(threads, recs)
