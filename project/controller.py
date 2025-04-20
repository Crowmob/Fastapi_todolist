from fastapi import APIRouter, Request, Response
from project.services.services import *
from project.schemas import *
from project.services.email_service import send_email
from project.auth import *

router = APIRouter()

@router.get("/")
async def homepage():
    return await getTasks()

# Get filtered tasks
@router.get("/filtered_tasks")
async def get_filtered_tasks():
    return await filteredTasks()

# Register
@router.post("/register")
async def register(log: Login, response: Response):
    user = await getUserId(log.username, log.password)
    if user:return {"message": "You have been already registered! Login."}
    await createUser(log.username, log.password)
    data = {"username": log.username, "password": log.password}
    token = create_token(data)
    response.set_cookie(key="user", value=token, max_age=1800)
    return "You are registered!"

# Login
@router.post("/login")
async def login(log: Login, response: Response):
    user = await getUserId(log.username, log.password)
    if not user: return {"message": "You don't have an account! Register."}
    data = {"username": log.username, "password": log.password}
    token = create_token(data)
    response.set_cookie(key="user", value=token, max_age=1800)
    return "You are logged in!"

# Add task
@router.post("/{username}/add")
async def add_task(task, request: Request, username: str):
    res = await check_user(request, username, None)
    if len(res) == 1: return res
    user_id = res[0]
    await createTask(task, user_id)
    return {"message": "Added task successfully"}

# Delete task
@router.delete("/{username}/delete")
async def delete_task(data: DeleteRequest, username: str, request: Request):
    res = await check_user(request, username, data)
    if len(res) == 1: return res
    user_id, is_task = res
    if is_task is None:
        return {"message": "You don't have this task."}
    else:
        await deleteTask(data.task, user_id)
        return {"message": "Deleted task successfully"}

# Update checkbox
@router.put("/{username}/checkbox")
async def update_checkbox(request: Request, username: str, data: UpdateRequest):
    res = await check_user(request, username, data)
    if len(res) == 1: return res
    user_id, is_task = res
    if is_task is None:
        return {"message": "You don't have this task."}
    else:
        await updateChecked(data.task, data.is_done, user_id)
        return {"message": "Updated checkbox"}

# Send email
@router.put("/send-email")
def sendEmail(email_data: SendEmail):
    return send_email(email_data)

# Disconnect database
@router.on_event("shutdown")
async def shutdown():
    await disconnect_db()