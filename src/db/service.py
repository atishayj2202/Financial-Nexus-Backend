from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session


class DBservice:
    @classmethod
    def update_bank_balance(cls, db: Session, amount: float, id: UUID):
        db.execute(
            text("UPDATE banks SET balance = balance + :amount WHERE id = :id"),
            {"amount": amount, "id": id},
        )
