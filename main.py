from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.tasks import *

# Load app
app = FastAPI()
app.include_router(router)
# Load templates
templates = Jinja2Templates(directory="templates")
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Connect to database
@app.on_event("startup")
async def startup():
    await connect_db()

# Disconnect database
@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# Main page
@app.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html",{
        "request": request,
        "tasks": await get_tasks()
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


