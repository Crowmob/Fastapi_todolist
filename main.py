from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from prisma import Prisma
from pydantic import BaseModel

# Load app
app = FastAPI()
# Load database
db = Prisma()
# Load templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Connect to database when the server started
@app.on_event("startup")
async def startup():
    await db.connect()

# Disconnect database when closing the server
@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

# Main page
@app.get("/")
async def homepage(request: Request):
    tasks = await db.item.find_many()
    tasks = [(task.id, task.item, task.checked) for task in tasks]
    print(tasks)
    return templates.TemplateResponse("index.html",{
        "request": request,
        "tasks": tasks
    })

# Get task
@app.post("/add")
async def submit_form(task: str = Form(...)):
    await db.item.create({"item": task, "checked": False})
    return RedirectResponse(url="/", status_code=303)

class DeleteRequest(BaseModel):
    task_id: int
    update: bool

@app.delete("/delete")
async def delete_task(data: DeleteRequest):
    print(data.task_id)
    await db.item.delete(where={"id": data.task_id})
    return {"message": "Deleted task successfully"}
# Update checkbox
@app.put("/checkbox")
async def update_checkbox(data: DeleteRequest):
    await db.item.update(data={"checked": data.update}, where={"id": data.task_id})
    tasks = await db.item.find_many()
    tasks = [(task.id, task.item, task.checked) for task in tasks]
    print(tasks)
    return {"message": "Updated checkbox"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


