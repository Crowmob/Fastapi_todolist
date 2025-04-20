from project.repository import *
from project.auth import *

async def createTask(task, user_id):
     await create_task(task, user_id)

async def getTasks():
    return await get_tasks()

async def updateChecked(task, is_done, user_id):
    await update_checked(task, is_done, user_id)

async def deleteTask(task, user_id):
    await delete_task(task, user_id)

async def getTask(task, user_id):
    return await get_task(task, user_id)

async def getUserId(username, password):
    users = await get_user(username)
    for user in users:
        if check_password(password.encode("utf-8"), user["password"].encode("utf-8")):
            return user["id"]
    return None

async def filteredTasks():
    return await filtered_tasks()

async def createUser(username, password):
    password = hash_password(password)
    await create_user(username, password.decode("utf-8"))