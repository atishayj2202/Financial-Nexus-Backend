from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class CreditCard(DBSchemaBase):
    user_id: UUID
    name: str
    card_name: str
    disabled: datetime | None = None
    pending: float = 0.0
    credit_limit: float
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _CreditCard


_CreditCard = Base.from_schema_base(CreditCard, "cards")
