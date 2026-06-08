from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base

if TYPE_CHECKING:
    from app.models.task import TaskItem


class TaskStage(Base):
    __tablename__ = "task_stages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    task_item_id: Mapped[int] = mapped_column(
        ForeignKey("task_items.id"),
        nullable=False,
    )
    stage_name: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_status: Mapped[str] = mapped_column(String(50), nullable=False)
    last_updated_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    task_item: Mapped[Optional["TaskItem"]] = relationship(
        back_populates="stages",
    )
