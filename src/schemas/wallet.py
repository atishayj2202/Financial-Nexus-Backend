from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateBankRequest(BaseModel):
    name: str
    bank_name: str
    opening_balance: float
    remarks: str | None = None


class BankResponse(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    bank_name: str
    balance: float
    remarks: str | None = None
    disabled: datetime | None = None


class CreateCreditCardRequest(BaseModel):
    name: str
    card_name: str
    card_limit: float
    remarks: str | None = None


class CreditCardResponse(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    card_name: str
    card_limit: float
    pending_limit: float
    balance: float
    remarks: str | None = None
    disabled: datetime | None = None
