import hashlib
from pathlib import Path

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin123"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_login(request: Request) -> int | RedirectResponse:
    user_id = request.session.get("user_id")
    if user_id is None:
        return RedirectResponse(url="/auth/login", status_code=303)
    return user_id


def ensure_default_user(db: Session) -> None:
    user_count = db.scalar(select(User).limit(1))
    if user_count is None:
        db.add(
            User(
                username=DEFAULT_USERNAME,
                password=hash_password(DEFAULT_PASSWORD),
            )
        )
        db.commit()


@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None},
    )


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.username == username))

    if user and user.password == hash_password(password):
        request.session["user_id"] = user.id
        request.session["username"] = user.username
        return RedirectResponse(url="/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": "Invalid Login"},
    )
