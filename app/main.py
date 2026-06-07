from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.database.db import SessionLocal, init_db
from app.models import ReminderLog, TaskItem, TaskStage, User  # noqa: F401
from app.routers import auth
from app.routers.auth import ensure_default_user

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        ensure_default_user(db)
    finally:
        db.close()
    yield


app = FastAPI(title="AI Task Manager", lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key="ai-task-manager-secret-key")
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"title": "AI Task Manager"},
    )


@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"title": "AI Task Manager"},
    )
