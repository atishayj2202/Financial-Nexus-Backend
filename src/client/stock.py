import yfinance as yf
from starlette.exceptions import HTTPException

from src.schemas.investment import StockSymbolResponse


class stockClient:
    @classmethod
    def get_stock_data(cls, symbol: str) -> StockSymbolResponse:
        data = yf.Ticker(symbol).info
        if "open" not in data:
            data = yf.Ticker(symbol + ".NS").info
        if "open" not in data:
            data = yf.Ticker(symbol + ".BO").info
        try:
            return StockSymbolResponse(
                name=data["longName"],
                currency=data["financialCurrency"]
                if "financialCurrency" in data
                else data["currency"],
                price=data["open"],
                symbol=data["symbol"],
            )
        except:
            raise HTTPException(status_code=404, detail="Stock not found")


if __name__ == "__main__":
    print(stockClient.get_stock_data("ADANIENT"))
