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
async def get_user(username, password):
    async with async_session_maker() as session:
        user = await session.execute(
            text("SELECT id FROM users WHERE username=:username AND password=:password"),
            {"username": username, "password": password})
        rows = user.fetchall()
        return [dict(row._mapping) for row in rows]

# Create user
async def create_user(username, password):
    async with async_session_maker() as session:
        await session.execute(text("INSERT INTO users (username, password) VALUES (:username, :password)"),
                              {"username": username, "password": password})
        await session.commit()

# Get tasks created between 8am and 8pm and starts with A
async def filtered_tasks():
    async with async_session_maker() as session:
        tasks = await session.execute(text("SELECT id, task, is_done, assigned_at, user_id FROM tasks WHERE "
                                           "EXTRACT(HOUR FROM assigned_at) BETWEEN 8 AND 20 AND task LIKE 'A%'"))
        return [[task.id, task.task, task.is_done, task.assigned_at, task.user_id] for task in tasks]






