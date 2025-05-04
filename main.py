from fastapi import FastAPI
from project.controller import *
import json
from project.cronjobs import start_job

# Load project
app = FastAPI(
    title="To-Do List",
    description="Manage your tasks to do",
    version="1.0.0",
)

app.include_router(router)

def save_openapi_json():
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=4)

save_openapi_json()
# Start cron job
start_job()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

