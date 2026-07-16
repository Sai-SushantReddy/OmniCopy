from fastapi import HTTPException, status

from app.core.redis import redis_client


RATE_LIMIT = 10
WINDOW = 60


def check_rate_limit(user_id: int):

    key = f"rate_limit:{user_id}"

    current = redis_client.incr(key)

    if current == 1:
        redis_client.expire(key, WINDOW)

    if current > RATE_LIMIT:
        ttl = redis_client.ttl(key)

        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds."
        )