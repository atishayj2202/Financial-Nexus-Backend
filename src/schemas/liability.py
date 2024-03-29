from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateEMIRequest(BaseModel):
    name: str
    bank_name: str
    monthly: float
    total_time: int
    remarks: str | None = None


class CreateLoanRequest(BaseModel):
    name: str
    bank_name: str
    amount: float
    remarks: str | None = None


class LoanResponse(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    bank_name: str
    paid: float
    total_amount: float
    remarks: str | None = None
    disabled: datetime | None = None


class EMIResponse(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    bank_name: str
    monthly: float
    pending: float
    total_time: int
    remarks: str | None = None
    disabled: datetime | None = None
