from db.database import *

# Create task
async def create_task(task):
    async with async_session_maker() as session:
        await session.execute(text("INSERT INTO tasks (task, checked) VALUES (:task, :checked);"), {"task": task, "checked": False})
        await session.commit()

# Read tasks
async def get_tasks():
    async with async_session_maker() as session:
        tasks = await session.execute(text('SELECT * FROM tasks;'))
        return [[task.id, task.task, task.checked] for task in tasks]

# Get task by id
async def get_task_by_id(id):
    async with async_session_maker() as session:
        task = await session.execute(text("SELECT * FROM tasks WHERE id = :id"), {"id": id})
        return task.fetchone()

# Update value of 'checked'
async def update_checked(data):
    async with async_session_maker() as session:
        await session.execute(text("UPDATE tasks SET checked = :checked WHERE id = :id"), {"id": data.task_id, "checked": data.update})
        await session.commit()

# Delete task by id
async def delete_task_by_id(id):
    async with async_session_maker() as session:
        await session.execute(text("DELETE FROM tasks WHERE id = :id"), {"id": id})
        await session.commit()


