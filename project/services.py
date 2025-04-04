from project.repository import *

async def createTask(task):
     await create_task(task)

async def getTasks():
    return await get_tasks()

async def updateChecked(data):
    await update_checked(data)

async def deleteTaskById(id):
    await delete_task_by_id(id)