from fastapi import Form, APIRouter
from fastapi.responses import RedirectResponse
from app.database import *
from app.schemas import *

router = APIRouter()

# Add task
@router.post("/add")
def submit_form(task: str = Form(...)):
    create_task(task)
    return RedirectResponse(url="/", status_code=303)

# Delete task
@router.delete("/delete")
def delete_task(data: DeleteRequest):
    delete_task_by_id(data.task_id)
    return {"message": "Deleted task successfully"}

# Update checkbox
@router.put("/checkbox")
def update_checkbox(data: UpdateRequest):
    update_checked(data)
    return {"message": "Updated checkbox"}