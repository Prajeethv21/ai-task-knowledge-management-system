from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.task import Task


def create_task(
    db: Session,
    title: str,
    description: str | None,
    assigned_to: int,
    created_by: int,
    status: str | None = None,
) -> Task:
    task = Task(
        title=title,
        description=description,
        assigned_to=assigned_to,
        created_by=created_by,
        status=status or "pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session, status_filter: str | None, assigned_to: int | None, for_user_id: int | None) -> list[Task]:
    query = db.query(Task)
    if for_user_id is not None:
        query = query.filter(Task.assigned_to == for_user_id)
    if status_filter:
        query = query.filter(Task.status == status_filter)
    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)
    return query.order_by(Task.created_at.desc()).all()


def update_task(db: Session, task: Task, status: str | None, description: str | None) -> Task:
    if status:
        task.status = status
    if description is not None:
        task.description = description
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
