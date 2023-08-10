import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    username: str


class UserRequest(UserBase):
    hashed_password: str


class UserResponse(UserBase):
    id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    hashed_password: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

    class Config:
        from_attributes = True


class AccessTokenResponse(BaseModel):
    access_token: str

    class Config:
        from_attributes = True
