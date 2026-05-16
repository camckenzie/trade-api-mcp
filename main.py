"""
Remember to run the following in the terminal before starting anything

source .venv/Scripts/activate -> use this if running it git bash

.venv\Scripts\activate -> use this if running in powershell 
- Recommend running in powershell as INFO is written more clearly

To actually run your program, run the following in your terminal:
uvicorn main:app --reload

To stop everything, run CTRL + C in terminal
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Trade(BaseModel):
    symbol: str
    price: float
    timestamp: str

trades_db = [
    {"symbol": "AAPL", "price": 189.50, "timestamp": "2025-05-10T09:30:00"},
    {"symbol": "MSFT", "price": 415.20, "timestamp": "2025-05-10T09:30:01"},
    {"symbol": "GOOG", "price": 172.80, "timestamp": "2025-05-10T09:30:02"},
]

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/trades")
def get_trades():
    return trades_db

@app.get("/trades/{symbol}")
def get_trade_by_symbol(symbol: str):
    result = [t for t in trades_db if t["symbol"] == symbol.upper()]
    return result if result else {"error": f"No trades found for {symbol}"}

@app.post("/trades")
def add_trade(trade: Trade):
    trades_db.append(trade.model_dump())
    return {"message": "Trade added", "trade": trade}