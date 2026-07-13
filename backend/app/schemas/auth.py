import uuid
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str = "user"
    department: str | None = None


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    name: str
    role: str
    department: str | None = None
    is_active: bool

    class Config:
        from_attributes = True
