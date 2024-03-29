from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.schemas.liability import CreateEMIRequest, CreateLoanRequest
from src.utils.enums import HolderType


class IncomeRequest(BaseModel):
    amount: float
    remarks: str | None = None
    to_account_id: UUID


class ExpenseRequest(BaseModel):
    name: str
    price: float
    amount: float | None = None
    remarks: str | None = None
    from_account_id: UUID | None = None
    from_credit_card_id: UUID | None = None
    from_loan: CreateLoanRequest | None = None
    from_emi: CreateEMIRequest | None = None


class ShortTransactionResponse(BaseModel):
    id: UUID
    created_at: datetime
    amount: float
    remarks: str | None = None
    transaction_type: HolderType


class CreateTransactionRequest(BaseModel):
    amount: float | None = None
    remarks: str | None = None
    from_account_id: UUID | None = None
    from_credit_card_id: UUID | None = None
    from_loan: CreateLoanRequest | None = None
    from_emi: CreateEMIRequest | None = None


class CreateTransferTransactionRequest(BaseModel):
    amount: float
    remarks: str | None = None
    to_account_id: UUID | None = None
    to_credit_card_id: UUID | None = None
    to_loan_id: UUID | None = None
    to_emi_id: UUID | None = None
