from project.repository import *
from project.auth import *
import json
from project.redis_init import redis_client

async def isSessionValid(user_agent, ip):
    session = None
    async for key in redis_client.scan_iter(match="session:*"):
        value = await redis_client.get(key)
        if value is None: continue

        session_data = json.loads(value)
        if session_data.get("user-agent") == user_agent and session_data.get("ip") == ip:
            session = {
                "session_id": key.decode().split("session:")[1],
                "session_data": session_data
            }
            break

    return session

async def createOrUpdateSession(session_data, expiry_time):
    session = await isSessionValid(session_data["user-agent"], session_data["ip"])
    if session:
        session["session_data"]["expired_at"] = datetime.fromisoformat(session["session_data"]["expired_at"])
        session["session_data"]["refresh_time"] = datetime.fromisoformat(session["session_data"]["refresh_time"])
        # Refresh session
        new_expired_at = datetime.utcnow() + timedelta(minutes=expiry_time)
        await refresh_session(session["session_data"], new_expired_at)
        session["session_data"]["expired_at"] = new_expired_at
        print(session["session_data"])
        session_id = await get_session_id(session["session_data"])
        # Refresh redis
        session["session_data"]["expired_at"] = session["session_data"]["expired_at"].isoformat()
        session["session_data"]["refresh_time"] = session["session_data"]["refresh_time"].isoformat()
        await redis_client.set(f"session:{session_id}", json.dumps(session["session_data"]))
    else:
        session_data["refresh_time"] = datetime.utcnow() + timedelta(minutes=session_data["refresh_time"])
        session_data["expired_at"] = datetime.utcnow() + timedelta(minutes=session_data["expired_at"])
        # Add session to db
        await create_session(session_data)
        session_id = await get_session_id(session_data)

        # Add session to cache(Redis)
        seconds_until_refresh = int(session_data["refresh_time"].timestamp())
        session_data["expired_at"], session_data["refresh_time"] = session_data["expired_at"].isoformat(), session_data[
            "refresh_time"].isoformat()
        await redis_client.set(f"session:{session_id}", json.dumps(session_data), ex=seconds_until_refresh)