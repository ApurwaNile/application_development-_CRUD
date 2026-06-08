from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.task import TaskItem
from app.models.user import User
from app.routers.auth import get_db, require_login

router = APIRouter(prefix="/tasks", tags=["tasks"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("")
async def list_tasks(request: Request, db: Session = Depends(get_db)):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    tasks = db.scalars(
        select(TaskItem)
        .options(joinedload(TaskItem.assignee))
        .order_by(TaskItem.id)
    ).unique().all()
    users = db.scalars(select(User).order_by(User.username)).all()

    return templates.TemplateResponse(
        request=request,
        name="task_form.html",
        context={"tasks": tasks, "users": users},
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
