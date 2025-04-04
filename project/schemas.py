from pydantic import BaseModel

# Create models
class DeleteRequest(BaseModel):
    task_id: int
class UpdateRequest(BaseModel):
    task_id: int
    is_done: bool
class SendEmail(BaseModel):
    subject: str
    body: str
    to_email: str