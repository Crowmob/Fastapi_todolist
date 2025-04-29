from fastapi import APIRouter, Request, Response, HTTPException
from project.schemas import *
from project.services.tasks_services import *
from project.services.email_services import *
from project.services.user_services import *
from project.services.session_serivices import *
from project.auth import *

router = APIRouter()

@router.get("/")
async def homepage(request: Request):
    session = await isSessionValid(request.headers.get("user-agent"), request.client.host)
    if session:
        await createOrUpdateSession(session["session_data"], 30)
        tasks = await getTasks()
        if len(tasks) == 0: return {"message": "You don't have tasks. Add one!"}
        return tasks
    else:
        return {"message": "Login or Register!"}

# Get filtered tasks
@router.get("/filtered_tasks")
async def get_filtered_tasks(request: Request):
    session = await isSessionValid(request.headers.get("user-agent"), request.client.host)
    if session:
        await createOrUpdateSession(session["session_data"], 30)
        return await filteredTasks()
    else: return {"message": "You are not logged in!"}

# Verify user
@router.get("/confirm/{token}")
async def verify_user(token, request: Request):
    user_data = decode_token(token)
    if user_data is None: return {"message": "Your verification time is expired."}
    user = await getUser(user_data["user_id"], None)
    if user[0]["is_verified"]: return {"message": "You are already verified"}
    await verifyUser(user_data["user_id"], user_data["password"])
    session_data = {"expired_at": 30, "refresh_time": 60, "user-agent": request.headers.get("user-agent"), "ip": request.client.host, "user_id": user_data["user_id"]}
    await createOrUpdateSession(session_data, 30)
    return {"message": "You are verified!"}

# Register
@router.post("/register")
async def register(log: Login):
    res = validate_email(log.email)
    if res is False: return {"message": res}
    user = await getUser(None, log.email)
    if len(user) == 0: await addUser(log.email, log.password)
    elif user[0]["is_verified"]: raise HTTPException(status_code=400, detail="You already have an account. Login")
    user = await getUser(None, log.email)
    token = create_token({"user_id": user[0]["id"], "password": log.password})
    send_verification_email(log.email, token, "Hello! Verify your email.")
    return {"message": "You are registered! Verification link was sent to your email."}


# Login
@router.post("/login")
async def login(log: Login, request: Request):
    user = await getUser(None, log.email)
    if not user: return {"message": "Account with this email does not exists. Register!"}
    if check_password(log.password, user[0]["password"]) is False: return "Wrong password!"
    if user[0]["is_verified"] is False: return {"message": "Your account is not verified!"}
    session_data = {"expired_at": 30, "refresh_time": 60, "user-agent": request.headers.get("user-agent"),
                    "ip": request.client.host, "user_id": user[0]["id"]}
    await createOrUpdateSession(session_data, 30)
    return {"message": "You are logged in!"}

# Add task
@router.post("/add")
async def add_task(data: TaskName, request: Request):
    session = await isSessionValid(request.headers.get("user-agent"), request.client.host)
    if session:
        await createOrUpdateSession(session["session_data"], 30)
        await createTask(data.task, session["session_data"]["user_id"])
    else: return {"message": "You are not logged in!"}
    return {"message": "Added task successfully"}

# Delete task
@router.delete("/delete")
async def delete_task(data: TaskName, request: Request):
    session = await isSessionValid(request.headers.get("user-agent"), request.client.host)
    if session:
        await createOrUpdateSession(session["session_data"], 30)
        task = await getTask(data.task, session["session_data"]["user_id"])
        if not task: return {"message": "You don't have this task"}
        await deleteTask(data.task, session["session_data"]["user_id"])
    else: return {"message": "You are not logged in!"}
    return {"message": "Deleted task successfully"}

# Update checkbox
@router.put("/checkbox")
async def update_checkbox(request: Request, data: UpdateRequest):
    session = await isSessionValid(request.headers.get("user-agent"), request.client.host)
    if session:
        await createOrUpdateSession(session["session_data"], 30)
        task = await getTask(data.task, session["session_data"]["user_id"])
        if not task: return {"message": "You don't have this task"}
        await updateChecked(data.task, data.is_done, session["session_data"]["user_id"])
    else: return {"message": "You are not logged in!"}
    return {"message": "Updated checkbox"}

# Disconnect database
@router.on_event("shutdown")
async def shutdown():
    await disconnect_db()