from redis.asyncio import Redis

redis_client = Redis.from_url("redis://redis-1:6379")