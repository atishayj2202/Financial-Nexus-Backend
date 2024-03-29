from pydantic import BaseModel


class StockResponse(BaseModel):
    name: str
    currency: str
    price: float
    symbol: str