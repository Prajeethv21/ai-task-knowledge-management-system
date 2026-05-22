from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.middleware.deps import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import authenticate_user
from app.services.activity_service import log_activity

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user, token = authenticate_user(db, payload.email, payload.password)
    log_activity(db, user_id=user.id, action="login", details="user login")
    return TokenResponse(access_token=token)
