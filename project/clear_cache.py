from redis_init import redis_client
import json
from datetime import datetime, timedelta
import asyncio

async def clear_sessions():
    async for key in redis_client.scan_iter(match="session:*"):
        value = await redis_client.get(key)
        if value is None: continue
        session_data = json.loads(value)
        if datetime.fromisoformat(session_data.get("refresh_time")) < datetime.utcnow():
            await redis_client.delete(key)
            return None
    print("Cleared session cache")
async def clear_unverified_users():
    async for key in redis_client.scan_iter(match="user:*"):
        value = await redis_client.get(key)
        if value is None: continue
        user_data = json.loads(value)
        if datetime.fromisoformat(user_data.get("registration_date")) > datetime.utcnow() + timedelta(hours=1):
            await redis_client.delete(key)
            return None
    print("Cleared user cache")

async def clear():
    await clear_sessions()
    await clear_unverified_users()
if __name__ == "__main__":
    asyncio.run(clear())