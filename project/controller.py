from fastapi import APIRouter
from project.services import *
from project.schemas import *

router = APIRouter()

@router.get("/")
def homepage():
    return getTasks()

# Add task
@router.post("/add")
def submit_form(task):
    createTask(task)
    return {"message": "Added task"}

# Delete task
@router.delete("/delete")
def delete_task(data: DeleteRequest):
    try:
        deleteTaskById(data.task_id)
        return {"message": "Deleted task successfully"}
    except:
        return {"message": "Task does not exists"}

# Update checkbox
@router.put("/checkbox")
def update_checkbox(data: UpdateRequest):
    try:
        updateChecked(data)
        return {"message": "Updated checkbox"}
    except:
        return {"message": "Task does not exists"}

# Disconnect database
@router.on_event("shutdown")
def shutdown():
    disconnect_db()