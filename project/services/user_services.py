from project.repository import *
from project.auth import *
from project.redis_init import redis_client
import uuid, json, datetime

async def getUser(id, email):
    user = await get_user(id, email)
    return user

async def addUser(email, password, registration_date):
    password = hash_password(password)
    registration_date = datetime.datetime.fromisoformat(registration_date)
    await create_user(email, password.decode("utf-8"), registration_date)

async def addUserToCache(email, password):
    password = hash_password(password)
    unique_id = str(uuid.uuid4())
    registration_date = datetime.datetime.utcnow()
    user_data = {"id": unique_id, "email": email, "password": password.decode("utf-8"), "registration_date": registration_date.isoformat()}
    await redis_client.set(f"user:{unique_id}", json.dumps(user_data), ex=3600)
    return unique_id

async def getUserFromCache(id):
    user = json.loads(await redis_client.get(f"user:{id}"))
    return user

async def deleteUserFromCache(id):
    await redis_client.delete(f"user:{id}")

async def verifyUser(id, password):
    password = hash_password(password)
    await verify_user(id, password.decode("utf-8"))