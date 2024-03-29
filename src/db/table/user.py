from typing import Type

from src.db.base import Base, DBSchemaBase


class User(DBSchemaBase):
    email: str | None
    name: str
    firebase_user_id: str

    @classmethod
    def _schema_cls(cls) -> Type[Base]:
        return _User


_User = Base.from_schema_base(User, "user_accounts")
