from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.middleware.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.search import SearchRequest, SearchResponse
from app.services.activity_service import log_activity
from app.services.search_service import semantic_search

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
def search(payload: SearchRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    results = semantic_search(payload.query, payload.top_k)
    log_activity(db, current_user.id, "search", payload.query)
    return {"results": results}
