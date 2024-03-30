from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.schemas.income import TransactionResponse
from src.schemas.liability import CreateEMIRequest, CreateLoanRequest


class StockSymbolResponse(BaseModel):
    name: str
    currency: str
    price: float
    symbol: str


class CreateStockInvestementRequest(BaseModel):
    symbol: str
    quantity: float
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


class StockResponse(BaseModel):
    id: UUID
    created_at: datetime
    symbol: str
    disabled: datetime | None = None
    quantity_left: float
    quantity_sold: float
    remarks: str | None = None
    transactions: list[TransactionResponse] | None = None


class FDResponse(BaseModel):
    id: UUID
    created_at: datetime
    disabled: datetime | None = None
    remarks: str | None = None
    bank_name: str
    initial_amount: float
    interest_rate: float
    sell_amount: float
    duration: float
    transactions: list[TransactionResponse] | None = None


class AssetResponse(BaseModel):
    id: UUID
    created_at: datetime
    disabled: datetime | None = None
    remarks: str | None = None
    name: str
    initial_amount: float
    sell_price: float
    transactions: list[TransactionResponse] | None = None
