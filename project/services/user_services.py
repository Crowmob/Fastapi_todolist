from project.repository import *
from project.auth import *

async def getUser(id, email):
    user = await get_user(id, email)
    return user

async def addUser(email, password):
    password = hash_password(password)
    await create_user(email, password.decode("utf-8"))

async def verifyUser(id, password):
    password = hash_password(password)
    await verify_user(id, password.decode("utf-8"))