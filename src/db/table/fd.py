from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class FD(DBSchemaBase):
    user_id: UUID
    bank_name: str
    disabled: datetime | None = None
    amount: float
    interest_rate: float
    duration: float
    sell_amount: float = 0.0
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _FD


_FD = Base.from_schema_base(FD, "fds")
