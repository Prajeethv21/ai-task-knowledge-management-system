from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog
from app.models.document import Document
from app.models.user import User
from app.models.task import Task


def get_analytics(db: Session) -> dict:
    total_tasks = db.query(func.count(Task.id)).scalar() or 0
    completed_tasks = db.query(func.count(Task.id)).filter(Task.status == "completed").scalar() or 0
    pending_tasks = db.query(func.count(Task.id)).filter(Task.status != "completed").scalar() or 0

    top_queries = (
        db.query(ActivityLog.details, func.count(ActivityLog.id).label("count"))
        .filter(ActivityLog.action == "search")
        .group_by(ActivityLog.details)
        .order_by(func.count(ActivityLog.id).desc())
        .limit(5)
        .all()
    )
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "top_queries": [{"query": q, "count": c} for q, c in top_queries],
    }


def get_dashboard(db: Session) -> dict:
    total_tasks = db.query(func.count(Task.id)).scalar() or 0
    completed_tasks = db.query(func.count(Task.id)).filter(Task.status == "completed").scalar() or 0
    pending_tasks = db.query(func.count(Task.id)).filter(Task.status != "completed").scalar() or 0
    documents_count = db.query(func.count(Document.id)).scalar() or 0

    recent_activity = (
        db.query(ActivityLog, User.email)
        .join(User, User.id == ActivityLog.user_id)
        .order_by(ActivityLog.created_at.desc())
        .limit(10)
        .all()
    )
    formatted = []
    for entry, email in recent_activity:
        formatted.append(
            {
                "id": entry.id,
                "user_id": entry.user_id,
                "action": entry.action,
                "details": entry.details,
                "created_at": entry.created_at.isoformat() if entry.created_at else "",
                "user_email": email,
            }
        )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "documents_count": documents_count,
        "recent_activity": formatted,
    }
