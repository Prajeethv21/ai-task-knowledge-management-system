from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.middleware.deps import get_db, require_role
from app.models.user import User
from app.schemas.analytics import AnalyticsOut, DashboardOut
from app.services.analytics_service import get_analytics, get_dashboard

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsOut)
def analytics(db: Session = Depends(get_db), current_user: User = Depends(require_role("Admin"))):
    return get_analytics(db)


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db), current_user: User = Depends(require_role("Admin"))):
    return get_dashboard(db)
