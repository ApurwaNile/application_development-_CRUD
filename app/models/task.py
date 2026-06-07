from datetime import date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

if TYPE_CHECKING:
    from app.models.reminder import ReminderLog
    from app.models.stage import TaskStage
    from app.models.user import User


class TaskItem(Base):
    __tablename__ = "task_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(Integer, nullable=False)
    assigned_to: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
    )
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    assignee: Mapped[Optional["User"]] = relationship(
        back_populates="task_items",
    )
    stages: Mapped[List["TaskStage"]] = relationship(
        back_populates="task_item",
        cascade="all, delete-orphan",
    )
    reminder_logs: Mapped[List["ReminderLog"]] = relationship(
        back_populates="task_item",
        cascade="all, delete-orphan",
    )
