from uuid import UUID

from pydantic import BaseModel


class PaymentRequest(BaseModel):
    amount: float
    from_account_id: UUID
    remarks: str | None = None


class SellStockRequest(BaseModel):
    remarks: str | None = None
    to_account_id: UUID
    quantity: float
    amount: float


class SellRequest(BaseModel):
    remarks: str | None = None
    to_account_id: UUID
    amount: float
