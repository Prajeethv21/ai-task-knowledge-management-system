from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    role_id: int


class UserOut(UserBase):
    id: int
    role_id: int
    role_name: str | None = None

    class Config:
        from_attributes = True
