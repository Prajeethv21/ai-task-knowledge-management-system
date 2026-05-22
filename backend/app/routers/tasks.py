from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.middleware.deps import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.activity_service import log_activity
from app.services.tasks_service import create_task, list_tasks, update_task, get_task

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskOut)
def create_task_endpoint(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("Admin")),
):
    task = create_task(
        db,
        payload.title,
        payload.description,
        payload.assigned_to,
        current_user.id,
        payload.status,
    )
    log_activity(db, current_user.id, "task_create", f"task_id={task.id}")
    return task


@router.get("", response_model=list[TaskOut])
def list_tasks_endpoint(
    status: str | None = None,
    assigned_to: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    for_user_id = None if current_user.role.name == "Admin" else current_user.id
    return list_tasks(db, status, assigned_to, for_user_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task_endpoint(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = get_task(db, task_id)
    if current_user.role.name != "Admin" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    updated = update_task(db, task, payload.status, payload.description)
    log_activity(db, current_user.id, "task_update", f"task_id={task.id}")
    return updated
