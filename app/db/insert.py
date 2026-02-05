import sqlite3
from datetime import date
from pathlib import Path
from app.db.db import get_connection

DB_PATH = Path("data/screener.db")

def get_connection():
    conn = sqlite3.connect(
        DB_PATH,
        timeout=30,              # <-- VERY important
        check_same_thread=False  # <-- FastAPI requirement
    )
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.row_factory = sqlite3.Row
    return conn


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def _to_float(value):
    try:
        if value in ("", "-", None):
            return None
        return float(value)
    except Exception:
        return None


def insert_stocks(stocks: list[dict], strategy: str):
    conn = get_connection()
    cursor = conn.cursor()

    run_date = date.today().isoformat()

    for stock in stocks:
        cursor.execute("""
            INSERT INTO stocks (
                company,
                symbol,
                current_price,
                pe,
                market_cap,
                dividend_yield,
                net_profit_qtr,
                qtr_profit_var_pct,
                sales_qtr_rs_cr,
                qtr_sales_var_pct,
                roce_pct,
                dma_50,
                dma_200,
                avg_pat_10y,
                strategy,
                run_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(symbol, strategy) DO UPDATE SET
                current_price = excluded.current_price,
                pe = excluded.pe,
                market_cap = excluded.market_cap,
                dividend_yield = excluded.dividend_yield,
                net_profit_qtr = excluded.net_profit_qtr,
                qtr_profit_var_pct = excluded.qtr_profit_var_pct,
                sales_qtr_rs_cr = excluded.sales_qtr_rs_cr,
                qtr_sales_var_pct = excluded.qtr_sales_var_pct,
                roce_pct = excluded.roce_pct,
                dma_50 = excluded.dma_50,
                dma_200 = excluded.dma_200,
                avg_pat_10y = excluded.avg_pat_10y,
                run_date = excluded.run_date
        """, (
            stock.get("company"),
            stock.get("symbol"),
            _to_float(stock.get("current_price")),
            _to_float(stock.get("pe")),
            _to_float(stock.get("market_cap")),
            _to_float(stock.get("dividend_yield")),
            _to_float(stock.get("net_profit_qtr")),
            _to_float(stock.get("qtr_profit_var_pct")),
            _to_float(stock.get("sales_qtr_rs_cr")),
            _to_float(stock.get("qtr_sales_var_pct")),
            _to_float(stock.get("roce_pct")),
            _to_float(stock.get("dma_50")),
            _to_float(stock.get("dma_200")),
            _to_float(stock.get("avg_pat_10y")),
            strategy,
            run_date
        ))
    conn.commit()
    conn.close()

    print(f"💾 Stocks upserted for strategy '{strategy}'")
