from typing import Literal

from fastapi import APIRouter, Body

from beetle.models import Task
from beetle.constants import TaskStatus


router = APIRouter()


@router.post("/create")
async def create(
    src: str = Body(),
    dst: str = Body(),
    interval: int = Body(ge=300),
    cleanup: bool = Body(),
):
    task = await Task.filter(src=src, dst=dst).first()
    if task:
        return {"error": "task already exists"}
    task = await Task.create(
        src=src,
        dst=dst,
        interval=interval,
        cleanup=cleanup,
        status=TaskStatus.running,
    )
    return task


@router.post("/update")
async def update(
    id: int = Body(),
    src: str = Body(),
    dst: str = Body(),
    interval: int = Body(le=60),
    cleanup: bool = Body(),
    status: Literal[TaskStatus.running, TaskStatus.stopped] = Body(),
):
    rows = await Task.filter(id=id).update(
        src=src,
        dst=dst,
        interval=interval,
        cleanup=cleanup,
        status=status,
    )
    return rows


@router.post("/delete")
async def delete(id: int = Body(embed=True)):
    rows = await Task.filter(id=id).delete()
    return rows


@router.post("/reads")
async def reads(constraints: dict = Body(default={})):
    tasks = await Task.filter(**constraints).all()
    return tasks
