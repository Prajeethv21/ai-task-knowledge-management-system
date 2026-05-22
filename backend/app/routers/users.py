from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.middleware.deps import get_db, get_current_user, require_role
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(require_role("Admin"))):
    users = db.query(User).order_by(User.id.asc()).all()
    response = []
    for user in users:
        response.append(UserOut(id=user.id, email=user.email, role_id=user.role_id, role_name=user.role.name))
    return response


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        email=current_user.email,
        role_id=current_user.role_id,
        role_name=current_user.role.name,
    )