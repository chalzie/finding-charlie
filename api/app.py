from typing import Union

from api.db import init_db, get_session
from api.models import Outpost, Task, TaskCreate, TaskRead, TaskUpdate

from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/v1")
async def root():
    return {"message": "Hello World!"}


@app.get("/api/v1/outposts")
async def get_outposts(session: Session = Depends(get_session)):
    outposts = session.exec(select(Outpost)).all()

    return {
        "outposts": [
            Outpost(
                name=o.name,
                task_id=o.task_id,
                open_at=o.open_at,
                started_at=o.started_at,
                completed_at=o.completed_at,
            )
            for o in outposts
        ]
    }


@app.get("/api/v1/outposts/{outpost_id}")
def get_outpost(outpost_id: int, q: Union[str, None]):
    return {"id": outpost_id, "q": q}


@app.post("/api/v1/outposts")
def create_outpost(outpost: Outpost):
    return "hehe"


@app.get("/api/v1/tasks", response_model=list[TaskRead])
def get_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return tasks


@app.get("/api/v1/tasks/{task_id}", response_model=TaskRead)
def get_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/api/v1/tasks", response_model=TaskRead)
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.patch("/api/v1/tasks/{task_id}", response_model=TaskRead)
def update_task(
    *, session: Session = Depends(get_session), task_id: int, task: TaskUpdate
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # exlude_unset -> only provided values
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/api/v1/tasks/{task_id}")
def delete_task(*, session: Session = Depends(get_session), task_id: int):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
