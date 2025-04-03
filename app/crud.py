from app.database import *

# Create task
def create_task(task):
    task = Tasks(task, False)
    session.add(task)
    session.commit()

# Read tasks
def get_tasks():
    tasks = session.query(Tasks).all()
    return [[task.id, task.task, task.checked] for task in tasks]

# Update value of 'checked'
def update_checked(data):
    task = session.query(Tasks).filter(Tasks.id == data.task_id).first()
    task.checked = data.update
    session.commit()

# Delete task by id
def delete_task_by_id(id):
    task = session.query(Tasks).filter(Tasks.id == id).first()
    session.delete(task)
    session.commit()

