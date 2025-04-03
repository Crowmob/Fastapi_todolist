from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from project.controller import *

# Load project
app = FastAPI()
app.include_router(router)
# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


