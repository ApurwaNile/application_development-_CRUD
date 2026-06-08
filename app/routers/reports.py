from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.routers.auth import get_db, require_login
from app.models.task import TaskItem
from app.models.stage import TaskStage

router = APIRouter(prefix="/reports", tags=["reports"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.get("/")
async def reports_page(
    request: Request,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result

    report_rows = db.execute(
        select(TaskStage, TaskItem)
        .join(TaskItem, TaskStage.task_item_id == TaskItem.id)
    ).all()

    return templates.TemplateResponse(
    request=request,
    name="reports.html",
    context={
        "report_rows": report_rows,
    },
)