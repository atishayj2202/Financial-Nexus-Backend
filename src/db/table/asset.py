from datetime import datetime
from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Asset(DBSchemaBase):
    user_id: UUID
    name: str
    disabled: datetime | None = None
    amount: float
    sell_price: float = 0.0
    buy_transaction: UUID
    sell_transaction: UUID | None = None
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Asset


_Asset = Base.from_schema_base(Asset, "assets")
