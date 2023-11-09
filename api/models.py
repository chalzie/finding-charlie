from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class OutpostBase(SQLModel):
    name: str
    task_id: int = Field(foreign_key="tasks.id")
    open_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class Outpost(OutpostBase, table=True):
    __tablename__ = "outposts"
    id: Optional[int] = Field(primary_key=True)


class OutpostCreate(OutpostBase):
    pass


class OutpostRead(OutpostBase):
    id: int


class OutpostUpdate(OutpostBase):
    name: Optional[str]
    task_id: Optional[str]


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
