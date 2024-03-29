from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Expense(DBSchemaBase):
    user_id: UUID
    name: str
    amount: float
    disabled: datetime | None = None
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Expense


_Expense = Base.from_schema_base(Expense, "expenses")
