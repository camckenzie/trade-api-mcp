"""
Remember to run the following in the terminal before starting anything

source .venv/Scripts/activate -> use this if running it git bash

.venv\Scripts\activate -> use this if running in powershell 
- Recommend running in powershell as INFO is written more clearly

To actually run your program, run the following in your terminal:
uvicorn main:app --reload

To stop everything, run CTRL + C in terminal
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel

# ── Database setup ────────────────────────────────────────
DATABASE_URL = "sqlite:///./trades.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Database model ────────────────────────────────────────
"""TradeDB is the database model.
It defines what the trades table looks like in SQLite.
In other words it defines how data is stored.

Each 'Column' maps to a column in the table.
SQLAlchemy is what is allowing us to 
define database in Python instead of raw SQL.
"""
class TradeDB(Base):
    __tablename__ = "trades"
    id        = Column(Integer, primary_key=True, index=True)
    symbol    = Column(String, index=True)
    price     = Column(Float)
    timestamp = Column(String)

Base.metadata.create_all(bind=engine)

# ── Pydantic schema ───────────────────────────────────────
"""Trade defines what the API accepts and returns.
Keep Trade and TradeDB separate so we can change one
without breaking the other."""
class Trade(BaseModel):
    symbol: str
    price: float
    timestamp: str

# ── DB session dependency ─────────────────────────────────
"""A dependency that gives each request its own database session
and closes it cleanly when the request is done.

The 'yield' makes it work. Everything before yield runs before the request.
Everything after runs after.
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── App ───────────────────────────────────────────────────
"""Depends(get_db) in each endpoint is FastAPI's dependency injection
This automatically calls get_db() and passes the session into the function"""

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/trades")
def get_trades(db: Session = Depends(get_db)):
    return db.query(TradeDB).all()

@app.get("/trades/{symbol}")
def get_trade_by_symbol(symbol: str, db: Session = Depends(get_db)):
    trades = db.query(TradeDB).filter(TradeDB.symbol == symbol.upper()).all()
    if not trades:
        raise HTTPException(status_code=404, detail=f"No trades found for {symbol}")
    return trades

@app.post("/trades")
def add_trade(trade: Trade, db: Session = Depends(get_db)):
    db_trade = TradeDB(
        symbol=trade.symbol.upper(),
        price=trade.price,
        timestamp=trade.timestamp
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade