import sqlite3
from datetime import date
from pathlib import Path

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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    run_date = date.today().isoformat()

    for stock in stocks:
        cursor.execute("""
            INSERT INTO stocks (
                company,
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
                strategy,
                run_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(company, strategy) DO UPDATE SET
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
                run_date = excluded.run_date
        """, (
            stock.get("company"),
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
            strategy,
            run_date
        ))

    conn.commit()
    conn.close()

    print(f"💾 Stocks upserted for strategy '{strategy}'")
