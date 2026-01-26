import sqlite3
from pathlib import Path

# Database location
DB_PATH = Path("data/screener.db")


def init_db():
    """
    Initialize SQLite database for Screener results.
    Stores full extracted columns + metadata for analysis.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Main stocks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            -- Identity
            company TEXT NOT NULL,

            -- Price & Valuation
            current_price REAL,          -- col_1
            pe REAL,                     -- col_2
            market_cap REAL,             -- col_3
            dividend_yield REAL,         -- col_4

            -- Quarterly Performance
            net_profit_qtr REAL,         -- col_5
            qtr_profit_var_pct REAL,     -- col_6
            sales_qtr_rs_cr REAL,        -- col_7
            qtr_sales_var_pct REAL,      -- col_8

            -- Efficiency & Trend
            roce_pct REAL,               -- col_9
            dma_50 REAL,                 -- col_10
            dma_200 REAL,                -- col_11

            -- Metadata
            strategy TEXT,               -- which screener strategy
            run_date TEXT                -- YYYY-MM-DD
        )
    """)

    # Optional index for faster queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_stocks_company
        ON stocks(company)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_stocks_strategy_date
        ON stocks(strategy, run_date)
    """)

    conn.commit()
    conn.close()

    print(f"✅ Database initialized successfully at: {DB_PATH.resolve()}")


if __name__ == "__main__":
    init_db()
