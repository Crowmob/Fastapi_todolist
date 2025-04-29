from pydantic import BaseModel

# Create models
class TaskName(BaseModel):
    task: str
class UpdateRequest(BaseModel):
    task: str
    is_done: bool
class SendEmail(BaseModel):
    subject: str
    body: str
    to_email: str

class Login(BaseModel):
    email: str
    password: str