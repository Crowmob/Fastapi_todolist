from sqlalchemy import create_engine, Column, String, INTEGER, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    task = Column("task", String, nullable=False)
    checked = Column("checked", Boolean, default=False)
    def __init__(self, task, checked):
        self.task = task
        self.checked = checked