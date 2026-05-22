from pydantic import BaseModel


class AnalyticsOut(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    top_queries: list[dict]


class ActivityOut(BaseModel):
    id: int
    user_id: int
    action: str
    details: str | None = None
    created_at: str
    user_email: str | None = None


class DashboardOut(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    documents_count: int
    recent_activity: list[ActivityOut]
