from datetime import datetime
from typing import List, Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase


class Stock(DBSchemaBase):
    user_id: UUID
    symbol: str
    disabled: datetime | None = None
    amount: float
    buy_price: float
    avg_sell_price: float = 0.0
    already_sold: float = 0.0
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Stock


_Stock = Base.from_schema_base(Stock, "stocks")
