from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase
from src.utils.enums import HolderType


class Transaction(DBSchemaBase):
    from_account_id: UUID | None = None
    from_account_type: HolderType
    to_account_id: UUID | None = None
    to_account_type: HolderType
    amount: float
    user_id: UUID
    remarks: str | None = None

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Transaction


_Transaction = Base.from_schema_base(Transaction, "transactions")
