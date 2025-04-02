from fastapi import Form, APIRouter
from fastapi.responses import RedirectResponse
from app.database import *
from app.schemas import *

router = APIRouter()

# Add task
@router.post("/add")
async def submit_form(task: str = Form(...)):
    await create_task(task)
    return RedirectResponse(url="/", status_code=303)

# Delete task
@router.delete("/delete")
async def delete_task(data: DeleteRequest):
    await delete_task_by_id(data.task_id)
    return {"message": "Deleted task successfully"}

# Update checkbox
@router.put("/checkbox")
async def update_checkbox(data: UpdateRequest):
    await update_checked(data)
    return {"message": "Updated checkbox"}