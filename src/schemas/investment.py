from uuid import UUID

from pydantic import BaseModel

from src.schemas.liability import CreateEMIRequest, CreateLoanRequest


class StockSymbolResponse(BaseModel):
    name: str
    currency: str
    price: float
    symbol: str


class CreateStockInvestementRequest(BaseModel):
    symbol: str
    quantity: int
    remarks: str | None = None
    from_account_id: UUID
    amount: float


class StockInvestmentResponse(BaseModel):
    id: UUID
    symbol: StockSymbolResponse
    quantity: int
    remarks: str | None = None
    from_account_id: UUID
    initial_amount: float


class DisolveStockInvestmentRequest(BaseModel):
    remarks: str | None = None
    to_account_id: UUID
    amount: float


class CreateFDRequest(BaseModel):
    amount: float
    bank_name: str
    remarks: str | None = None
    from_account_id: UUID
    duration: int
    interest_rate: float


class CreateAssetRequest(BaseModel):
    name: str
    price: float
    amount: float | None = None
    remarks: str | None = None
    from_account_id: UUID | None = None
    from_credit_card_id: UUID | None = None
    from_loan: CreateLoanRequest | None = None
    from_emi: CreateEMIRequest | None = None
