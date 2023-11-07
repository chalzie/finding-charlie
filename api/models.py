from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Outpost(SQLModel, table=True):
    __tablename__ = "outposts"

    id: Optional[int] = Field(primary_key=True)
    task_id: int = Field(foreign_key="tasks.id")

    name: str
    open_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class TaskBase(SQLModel):
    task: str
    answer: str


class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(primary_key=True)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int


class TaskUpdate(TaskBase):
    task: Optional[str]
    answer: Optional[str]
