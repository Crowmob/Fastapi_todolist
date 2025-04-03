from fastapi import FastAPI
from project.controller import *
import json

# Load project
app = FastAPI(
    title="My To-Do List API",
    description="API documentation for managing to-do tasks",
    version="1.0.0",
)

app.include_router(router)

def save_openapi_json():
    with open("openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=4)

# Run this function at startup
save_openapi_json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


