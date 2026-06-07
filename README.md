# AI Task Manager

A task management application built with FastAPI, SQLAlchemy, SQLite, and Jinja2 templates.

## Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Frontend:** HTML, CSS, Bootstrap
- **Templating:** Jinja2

## Requirements

- Python 3.12

## Setup

```bash
cd ai-task-manager
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Project Structure

```
ai-task-manager/
├── app/
│   ├── main.py
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
├── requirements.txt
├── README.md
└── task_manager.db
```
