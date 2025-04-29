from project.repository import *

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

async def filteredTasks():
    return await filtered_tasks()