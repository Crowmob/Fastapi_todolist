from fastapi import APIRouter
from project.services.services import *
from project.schemas import *
from project.services.email_service import send_email

router = APIRouter()

@router.get("/")
async def homepage():
    return await getTasks()

# Add task
@router.post("/add")
async def add_task(task):
    await createTask(task)
    return {"message": "Added task successfully"}

# Delete task
@router.delete("/delete")
async def delete_task(data: DeleteRequest):
    task = await get_task_by_id(data.task_id)
    if task is None:
        return {"message": "Task does not exist"}
    else:
        await deleteTaskById(data.task_id)
        return {"message": "Deleted task successfully"}

# Update checkbox
@router.put("/checkbox")
async def update_checkbox(data: UpdateRequest):
    task = await get_task_by_id(data.task_id)
    if task is None:
        return {"message": "Task does not exist"}
    else:
        await updateChecked(data)
        return {"message": "Updated checkbox"}

@router.put("/send-email")
def sendEmail(email_data: SendEmail):
    return send_email(email_data)

# Disconnect database
@router.on_event("shutdown")
async def shutdown():
    await disconnect_db()