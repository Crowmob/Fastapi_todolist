from pydantic import BaseModel

# Create models
class DeleteRequest(BaseModel):
    task: str
class UpdateRequest(BaseModel):
    task: str
    is_done: bool
class SendEmail(BaseModel):
    subject: str
    body: str
    to_email: str

class Login(BaseModel):
    username: str
    password: str