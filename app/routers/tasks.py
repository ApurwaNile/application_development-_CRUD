from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.task import TaskItem
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

    return templates.TemplateResponse(
        request=request,
        name="task_form.html",
        context={"tasks": tasks},
    )
