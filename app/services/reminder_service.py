from datetime import datetime, date

from app.models.task import TaskItem
from app.models.reminder import ReminderLog


class ReminderService:

    @staticmethod
    def check_overdue_tasks(db):

        print("Running reminder check...")

        tasks = db.query(TaskItem).all()

        for task in tasks:

            print(
                f"Task {task.id} | Due={task.due_date} | Status={task.status}"
            )

            if task.status.lower() == "completed":
                continue

            if date.today() <= task.due_date:
                continue

            overdue_days = (date.today() - task.due_date).days

            print(f"EMAIL reminder for task {task.id}")

            db.add(
                ReminderLog(
                    task_item_id=task.id,
                    lesson_id=task.lesson_id,
                    reminder_type="EMAIL",
                    sent_date=datetime.now(),
                )
            )

            if overdue_days > 2:

                print(f"WHATSAPP reminder for task {task.id}")

                db.add(
                    ReminderLog(
                        task_item_id=task.id,
                        lesson_id=task.lesson_id,
                        reminder_type="WHATSAPP",
                        sent_date=datetime.now(),
                    )
                )

            if overdue_days > 5:

                print(f"IVR reminder for task {task.id}")

                db.add(
                    ReminderLog(
                        task_item_id=task.id,
                        lesson_id=task.lesson_id,
                        reminder_type="IVR",
                        sent_date=datetime.now(),
                    )
                )

        db.commit()