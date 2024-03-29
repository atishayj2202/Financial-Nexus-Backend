from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    created_at: datetime | None = None


class UserCreateRequest(BaseModel):
    email: str
    name: str
    firebase_user_id: str


class UserUpdateRequest(BaseModel):
    email: str | None = None
    name: str | None = None


class RatingRequest(BaseModel):
    rate: int
    comment: str | None = None
