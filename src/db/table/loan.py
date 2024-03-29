from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Loan(DBSchemaBase):
    user_id: UUID
    name: str
    bank_name: str
    disabled: datetime | None = None
    pending: float
    total_amount: int
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Loan


_Loan = Base.from_schema_base(Loan, "loans")
