from prisma import Prisma

# Load database
db = Prisma()

# Connect to database
async def connect_db():
    await db.connect()

# Disconnect database
async def disconnect_db():
    await db.disconnect()

# Get all tasks
async def get_tasks():
    tasks = await db.item.find_many()
    tasks = [(task.id, task.item, task.checked) for task in tasks]
    return tasks

# Delete task from database
async def delete_task_by_id(id):
    await db.item.delete(where={"id": id})

# Update 'checked' value
async def update_checked(data):
    await db.item.update(data={"checked": data.update}, where={"id": data.task_id})

# Create task
async def create_task(task):
    await db.item.create({"item": task, "checked": False})