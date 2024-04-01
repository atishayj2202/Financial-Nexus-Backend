from typing import Type
from uuid import UUID

from src.db.base import Base, DBSchemaBase
from src.utils.enums import MessageBy


class Message(DBSchemaBase):
    user_id: UUID
    message: str
    message_by: MessageBy

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _Message


_Message = Base.from_schema_base(Message, "messages")
