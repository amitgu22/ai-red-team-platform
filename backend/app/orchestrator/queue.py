import json, os
import redis

QUEUE_NAME = os.getenv("REDTEAM_QUEUE", "redteam:campaigns")

def client():
    return redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"), decode_responses=True)

def enqueue(campaign_id: int):
    client().rpush(QUEUE_NAME, json.dumps({"campaign_id": campaign_id}))

def dequeue(timeout: int = 5):
    item = client().blpop(QUEUE_NAME, timeout=timeout)
    return json.loads(item[1]) if item else None
