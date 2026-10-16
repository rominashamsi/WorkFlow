
import os

import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6380")),
    decode_responses=True,
    socket_connect_timeout=1,
    socket_timeout=1,
)
