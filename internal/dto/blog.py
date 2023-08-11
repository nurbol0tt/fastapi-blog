import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, EmailStr


class CategoryRequest(BaseModel):
    title: str


class CategoryResponse(CategoryRequest):
    id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class BlogBase(BaseModel):
    phone: str
    email: EmailStr
    text: str
    user: str
    fio: str


class ApplicationRequest(BlogBase):
    category_id: uuid.UUID


class ApplicationResponse(BlogBase):
    id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class ApplicationDetailRead(ApplicationResponse):

    class Config:
        from_attributes = True


class ApplicationReadAllResponse(BaseModel):
    applications: list[ApplicationResponse]


class CategoryAllResponse(BaseModel):
    categories: list[CategoryResponse]


class CategoryDetailResponse(CategoryResponse):
    id: Optional[uuid.UUID]
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True


@dataclass
class ApplicationFilter:

    phone: str = Query('')
    email: str = Query('')
