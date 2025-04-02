from sqlalchemy import create_engine, Column, String, INTEGER, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    task = Column("task", String, nullable=False)
    checked = Column("checked", Boolean, default=False)
    def __init__(self, task, checked):
        self.task = task
        self.checked = checked

engine = create_engine("sqlite:///tasks.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Close session
def disconnect_db():
    session.close()

# Get all tasks
def get_tasks():
    tasks = session.query(Tasks).all()
    return [[task.id, task.task, task.checked] for task in tasks]

# Delete task by id
def delete_task_by_id(id):
    task = session.query(Tasks).filter(Tasks.id == id).first()
    session.delete(task)
    session.commit()

# Update value of 'checked'
def update_checked(data):
    task = session.query(Tasks).filter(Tasks.id == data.task_id).first()
    task.checked = data.update
    session.commit()

# Create task
def create_task(task):
    task = Tasks(task, False)
    session.add(task)
    session.commit()
