from fastapi import Form, APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from project.services import *
from project.schemas import *

router = APIRouter()
# Load templates
templates = Jinja2Templates(directory="templates")

# Main page
@router.get("/")
def homepage(request: Request):
    return templates.TemplateResponse("index.html",{
        "request": request,
        "tasks": getTasks()
    })

# Add task
@router.post("/add")
def submit_form(task: str = Form(...)):
    createTask(task)
    return RedirectResponse(url="/", status_code=303)

# Delete task
@router.delete("/delete")
def delete_task(data: DeleteRequest):
    deleteTaskById(data.task_id)
    return {"message": "Deleted task successfully"}

# Update checkbox
@router.put("/checkbox")
def update_checkbox(data: UpdateRequest):
    updateChecked(data)
    return {"message": "Updated checkbox"}

# Disconnect database
@router.on_event("shutdown")
def shutdown():
    disconnect_db()