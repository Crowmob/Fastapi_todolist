from db.database import *

# Create task
async def create_task(task, user_id):
    async with async_session_maker() as session:
        await session.execute(text("INSERT INTO tasks (task, is_done, user_id) VALUES (:task, :is_done, :user_id);"), {"task": task, "is_done": False, "user_id": user_id})
        await session.commit()

# Read tasks
async def get_tasks():
    async with async_session_maker() as session:
        tasks = await session.execute(text('SELECT id, task, is_done, assigned_at, user_id FROM tasks;'))
        return [[task.id, task.task, task.is_done, task.assigned_at, task.user_id] for task in tasks]

# Get task by id
async def get_task(task, user_id):
    async with async_session_maker() as session:
        task = await session.execute(text("SELECT id, task, is_done, assigned_at, user_id FROM tasks WHERE task = :task AND user_id = :user_id"),
                                     {"task": task, "user_id": user_id})
        return task.fetchone()

# Update value of 'checked'
async def update_checked(task, is_done, user_id):
    async with async_session_maker() as session:
        await session.execute(text("UPDATE tasks SET is_done = :is_done WHERE task = :task AND user_id = :user_id"), {"task": task, "is_done": is_done, "user_id": user_id})
        await session.commit()

# Delete task by id
async def delete_task(task, user_id):
    async with async_session_maker() as session:
        await session.execute(text("DELETE FROM tasks WHERE task = :task AND user_id = :user_id"), {"task": task, "user_id": user_id})
        await session.commit()


# Get user
async def get_user(id, email):
    async with async_session_maker() as session:
        if id is None:
            user = await session.execute(
                text("SELECT id, email, password, is_verified FROM users WHERE email=:email"),
                {"email": email})
        elif email is None:
            user = await session.execute(
                text("SELECT id, email, password, is_verified FROM users WHERE id=:id"),
                {"id": id})
        rows = user.fetchall()
        return [dict(row._mapping) for row in rows]

# Create user
async def create_user(email, password):
    async with async_session_maker() as session:
        await session.execute(text("INSERT INTO users (email, password) VALUES (:email, :password)"),
                              {"email": email, "password": password})
        await session.commit()

# Verify user
async def verify_user(id, password):
    async with async_session_maker() as session:
        await session.execute(text("UPDATE users SET is_verified = true, password=:password WHERE id = :id"), {"id": id, "password": password})
        await session.commit()

# Get tasks created between 8am and 8pm and starts with A
async def filtered_tasks():
    async with async_session_maker() as session:
        tasks = await session.execute(text("SELECT id, task, is_done, assigned_at, user_id FROM tasks WHERE "
                           
                                           "EXTRACT(HOUR FROM assigned_at) BETWEEN 8 AND 20 AND task LIKE 'A%'"))
        return [[task.id, task.task, task.is_done, task.assigned_at, task.user_id] for task in tasks]

# Create session
async def create_session(data):
    async with async_session_maker() as session:
        await session.execute(text("""INSERT INTO sessions (expired_at, refresh_time, user_agent, ip, user_id)
                                    VALUES (:expired_at, :refresh_time, :user_agent, :ip, :user_id)"""),
                                    {"expired_at": data["expired_at"], "refresh_time": data["refresh_time"],
                                    "user_agent": data["user-agent"], "ip": data["ip"], "user_id": data["user_id"]})
        await session.commit()

# Get session's id
async def get_session_id(data):
    async with async_session_maker() as session:
        session_id = await session.execute(text("SELECT id FROM sessions WHERE expired_at=:expired_at AND "
                                          "refresh_time=:refresh_time AND user_agent=:user_agent AND ip=:ip AND user_id=:user_id"),
                                         {"expired_at": data["expired_at"],
                                          "refresh_time": data["refresh_time"],
                                          "user_agent": data["user-agent"], "ip": data["ip"], "user_id": data["user_id"]})
        return session_id.fetchall()[0][0]

# Refresh session
async def refresh_session(data, new_expired_at):
    async with async_session_maker() as session:
        await session.execute(text("UPDATE sessions SET expired_at = :new_expired_at WHERE expired_at=:expired_at AND "
                                   "refresh_time=:refresh_time AND user_agent=:user_agent AND ip=:ip AND user_id=:user_id"),
                              {"new_expired_at": new_expired_at, "expired_at": data["expired_at"], "refresh_time": data["refresh_time"],
                               "user_agent": data["user-agent"], "ip": data["ip"], "user_id": data["user_id"]})
        await session.commit()









