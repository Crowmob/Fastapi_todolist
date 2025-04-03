from pydantic import BaseModel

# Create models
class DeleteRequest(BaseModel):
    task_id: int
class UpdateRequest(BaseModel):
    task_id: int
    update: bool