import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class CategoryInput(BaseModel):
    title: str


class CategoryRead(CategoryInput):
    id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class BaseApplication(BaseModel):
    phone: str
    email: str
    text: str
    user: str
    fio: str


class ApplicationInput(BaseApplication):
    category_id: uuid.UUID


class ApplicationRead(BaseApplication):
    id: Optional[uuid.UUID]

    class Config:
        from_attributes = True


class ApplicationDetailRead(ApplicationRead):
    # categories: List[CategoryRead]

    class Config:
        from_attributes = True


class ApplicationReadAll(BaseModel):
    applications: list[ApplicationRead]


class CategoryReadAll(BaseModel):
    categories: list[CategoryRead]


class CategoryDetailRead(CategoryRead):
    id: Optional[uuid.UUID]
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        from_attributes = True


@dataclass
class ApplicationFilter:

    phone: str = Query('')
    email: str = Query('')
