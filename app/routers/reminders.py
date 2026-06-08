from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.routers.auth import get_db, require_login
from app.models.reminder import ReminderLog
from app.services.reminder_service import ReminderService

router = APIRouter(prefix="/reminders", tags=["reminders"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@router.post("/run")
async def run_reminders(
    request: Request,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)

    if isinstance(auth_result, RedirectResponse):
        return auth_result

    ReminderService.check_overdue_tasks(db)

    return RedirectResponse(
        url="/reminders",
        status_code=303,
    )


@router.get("")
async def reminder_logs(
    request: Request,
    db: Session = Depends(get_db),
):
    auth_result = require_login(request)

    if isinstance(auth_result, RedirectResponse):
        return auth_result

    logs = db.scalars(
        select(ReminderLog)
        .order_by(ReminderLog.sent_date.desc())
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="reminders.html",
        context={
            "logs": logs,
        },
    )