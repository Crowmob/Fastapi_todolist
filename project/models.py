from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import Column, String, INTEGER, Boolean, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column("id", INTEGER, primary_key=True, autoincrement=True)
    task = Column("task", String, nullable=False)
    is_done = Column("is_done", Boolean, default=False)
    def __init__(self, task, is_done):
        self.task = task
        self.is_done = is_done