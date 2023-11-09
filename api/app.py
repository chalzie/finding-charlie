# from typing import Union

from api.db import init_db, get_session
from api.models import Task, TaskCreate, TaskRead, TaskUpdate
from api.models import Outpost, OutpostCreate, OutpostRead, OutpostUpdate

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
def get_outposts(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100)
):
    outposts = session.exec(select(Outpost).offset(offset).limit(limit)).all()
    return outposts


@app.get("/api/v1/outposts/{outpost_id}")
def get_outpost(*, session: Session = Depends(get_session), outpost_id: int):
    outpost = session.get(Outpost, outpost_id)
    if not outpost:
        raise HTTPException(status_code=404, detail="Outpost not found")
    return outpost


@app.post("/api/v1/outposts", response_model=OutpostRead)
def create_outpost(
    *,
    session: Session = Depends(get_session),
    outpost: OutpostCreate
):
    db_outpost = Outpost.from_orm(outpost)
    session.add(db_outpost)
    session.commit()
    session.refresh(db_outpost)
    return db_outpost


@app.patch("/api/v1/outposts/{outpost_id}", response_model=OutpostRead)
def update_outpost(
    *,
    session: Session = Depends(get_session),
    outpost_id: int,
    outpost: OutpostUpdate
):
    db_outpost = session.get(Outpost, outpost_id)
    if not db_outpost:
        raise HTTPException(status_code=404, detail="Outpost not found")

    outpost_data = outpost.dict(exclude_unset=True)
    for key, value in outpost_data.items():
        setattr(db_outpost, key, value)

    session.add(db_outpost)
    session.commit()
    session.refresh(db_outpost)
    return db_outpost


@app.delete("/api/v1/outposts/{outpost_id}")
def delete_outpost(
    *,
    session: Session = Depends(get_session),
    outpost_id: int
):
    outpost = session.get(Outpost, outpost_id)
    if not outpost:
        raise HTTPException(status_code=404, detail="Outpost not found")
    session.delete(outpost)
    session.commit()
    return {"ok": True}


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
