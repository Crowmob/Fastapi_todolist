from project.repository import *

def createTask(task):
    create_task(task)

def getTasks():
    return get_tasks()

def updateChecked(data):
    update_checked(data)

def deleteTaskById(id):
    delete_task_by_id(id)