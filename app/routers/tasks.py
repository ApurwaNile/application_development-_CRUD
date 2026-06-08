from datetime import date ,datetime
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.task import TaskItem
from app.models.user import User
from app.routers.auth import get_db, require_login
from app.models.stage import TaskStage

router = APIRouter(prefix="/tasks", tags=["tasks"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

@router.get("")
async def list_tasks(
    request: Request,
    edit: int | None = None,
    search: int | None = None,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    query = (
        select(TaskItem)
        .options(joinedload(TaskItem.assignee))
    )

    if search is not None:
        query = query.where(TaskItem.id == search)

    tasks = db.scalars(
        query.order_by(TaskItem.id)
    ).unique().all()

    users = db.scalars(
        select(User).order_by(User.username)
    ).all()

    edit_task = None

    if edit is not None:
        edit_task = db.scalar(
            select(TaskItem).where(TaskItem.id == edit)
        )

    return templates.TemplateResponse(
        request=request,
        name="task_form.html",
        context={
            "tasks": tasks,
            "users": users,
            "edit_task": edit_task,
        },
    )

@router.post("")
async def create_task(
    request: Request,
    lesson_id: int = Form(...),
    assigned_to: str = Form(""),
    start_date: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    task = TaskItem(
        lesson_id=lesson_id,
        assigned_to=int(assigned_to) if assigned_to else None,
        start_date=date.fromisoformat(start_date),
        due_date=date.fromisoformat(due_date),
        status=status,
    )

    db.add(task)
    db.commit()

    return RedirectResponse(url="/tasks", status_code=303)

@router.post("/{task_id}/update")
async def update_task(
    request: Request,
    task_id: int,
    lesson_id: int = Form(...),
    assigned_to: str = Form(""),
    start_date: str = Form(...),
    due_date: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    task = db.scalar(select(TaskItem).where(TaskItem.id == task_id))
    if task is None:
        return RedirectResponse(url="/tasks", status_code=303)

    task.lesson_id = lesson_id
    task.assigned_to = int(assigned_to) if assigned_to else None
    task.start_date = date.fromisoformat(start_date)
    task.due_date = date.fromisoformat(due_date)
    task.status = status
    db.commit()

    return RedirectResponse(url="/tasks", status_code=303)

@router.post("/{task_id}/delete")
async def delete_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    task = db.scalar(select(TaskItem).where(TaskItem.id == task_id))

    if task is not None:
        db.delete(task)
        db.commit()

    return RedirectResponse(url="/tasks", status_code=303)

@router.get("/{task_id}/stages")
async def view_stages(
    request: Request,
    task_id: int,
    edit: int | None = None,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    task = db.scalar(
        select(TaskItem).where(TaskItem.id == task_id)
    )

    if task is None:
        return RedirectResponse(url="/tasks", status_code=303)

    stages = db.scalars(
        select(TaskStage)
        .where(TaskStage.task_item_id == task_id)
        .order_by(TaskStage.id)
    ).all()

    edit_stage = None

    if edit is not None:
        edit_stage = db.scalar(
            select(TaskStage).where(TaskStage.id == edit)
        )

    return templates.TemplateResponse(
        request=request,
        name="stage_form.html",
        context={
            "task": task,
            "stages": stages,
            "edit_stage": edit_stage,
        },
    )

@router.post("/{task_id}/stages")
async def create_stage(
    request: Request,
    task_id: int,
    stage_name: str = Form(...),
    stage_status: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    stage = TaskStage(
        task_item_id=task_id,
        stage_name=stage_name,
        stage_status=stage_status,
        last_updated_date=datetime.now(),
        status=status,
    )

    db.add(stage)
    db.commit()

    return RedirectResponse(
        url=f"/tasks/{task_id}/stages",
        status_code=303,
    )

@router.post("/{task_id}/stages/{stage_id}/update")
async def update_stage(
    request: Request,
    task_id: int,
    stage_id: int,
    stage_name: str = Form(...),
    stage_status: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    stage = db.scalar(
        select(TaskStage).where(TaskStage.id == stage_id)
    )

    if stage is None:
        return RedirectResponse(
            url=f"/tasks/{task_id}/stages",
            status_code=303,
        )

    stage.stage_name = stage_name
    stage.stage_status = stage_status
    stage.status = status
    stage.last_updated_date = datetime.now()

    db.commit()

    return RedirectResponse(
        url=f"/tasks/{task_id}/stages",
        status_code=303,
    )

@router.post("/{task_id}/stages/{stage_id}/delete")
async def delete_stage(
    request: Request,
    task_id: int,
    stage_id: int,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    stage = db.scalar(
        select(TaskStage).where(TaskStage.id == stage_id)
    )

    if stage:
        db.delete(stage)
        db.commit()

    return RedirectResponse(
        url=f"/tasks/{task_id}/stages",
        status_code=303,
    )