from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Bank(DBSchemaBase):
    user_id: UUID
    name: str
    bank_name: str
    disabled: datetime | None = None
    balance: float = 0
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Bank


_Bank = Base.from_schema_base(Bank, "banks")
