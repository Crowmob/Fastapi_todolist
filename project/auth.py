from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import bcrypt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Create token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30) # Expires after 30 minute
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token

# Decode and verify token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def check_user(request, username, data):
    from project.services.services import getUserId, getTask
    token = request.cookies.get("user")
    if token == None: return "You are not logged in! Login."
    user = decode_token(token)
    if username != user["username"]: return {"message": "You logged in with another account."}
    user_id = await getUserId(user["username"], user["password"])
    try: is_task = await getTask(data.task, user_id)
    except: is_task = None
    return user_id, is_task

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed

def check_password(password, hashed_password):
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False