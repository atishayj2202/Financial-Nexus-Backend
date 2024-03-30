from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.utils.enums import HolderType


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


class TransactionResponse(BaseModel):
    id: UUID
    created_at: datetime
    amount: float
    remarks: str | None = None
    transaction_type: str
    from_id: UUID | None = None
    from_type: HolderType | None = None
    to_id: UUID | None = None
    to_type: HolderType | None = None
