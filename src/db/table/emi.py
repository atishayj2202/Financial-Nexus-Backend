from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class EMI(DBSchemaBase):
    user_id: UUID
    name: str
    bank_name: str
    disabled: datetime | None = None
    pending: float
    monthly: float
    total_time: int
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _EMI


_EMI = Base.from_schema_base(EMI, "emis")
