# AI Task Manager

## Project Overview

AI Task Manager is a FastAPI-based web application developed as part of the AI Developer Internship evaluation. The system allows authenticated users to manage tasks, track workflow stages, generate reports, and run automated reminder checks for overdue tasks.

## Features

### Authentication

* User login
* Session-based authentication
* Protected routes

### Task Management

* Create Task
* View Tasks
* Update Task
* Delete Task
* Search Tasks

### Stage Management

* Create Task Stages
* View Task Stages
* Update Task Stages
* Delete Task Stages

### Reports Module

* Task and Stage reporting
* SQLAlchemy join between TaskItem and TaskStage
* Displays:

  * Stage ID
  * Task ID
  * Due Date
  * Last Updated Date
  * Status

### Reminder System

* Automated overdue task checking
* Email reminders for overdue tasks
* WhatsApp reminders for tasks overdue by more than 2 days
* IVR reminders for tasks overdue by more than 5 days
* Reminder log generation and storage

### Database

* SQLite database
* SQLAlchemy ORM
* Relationship mapping between:

  * Users
  * Tasks
  * Task Stages
  * Reminder Logs

## Technology Stack

* FastAPI
* SQLAlchemy
* SQLite
* Jinja2
* Bootstrap 5
* HTML/CSS

## Project Structure

```text
ai-task-manager/
├── app/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── templates/
│   └── static/
├── screenshots/
├── requirements.txt
├── README.md
└── task_manager.db
```

## Installation

```bash
git clone <repository-url>
cd ai-task-manager
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Demo Credentials

Username:

```text
admin
```

Password:

```text
admin123
```

## Screenshots

### Login Page

Insert screenshot here

### Task Management

Insert screenshot here

### Task Stages

Insert screenshot here

### Reports Module

Insert screenshot here

### Reminder Logs

Insert screenshot here

## Future Improvements

* Email service integration
* WhatsApp API integration
* Scheduled background reminders
* Dashboard analytics
* Duplicate reminder prevention
