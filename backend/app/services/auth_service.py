from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.security import verify_password, create_access_token


def authenticate_user(db: Session, email: str, password: str) -> tuple[User, str]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return user, token
