import sqlite3
from pathlib import Path
from datetime import date

from app.scoring.composite_score import composite_score

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def score_all_stocks():
    """
    Compute composite score for all stocks
    and upsert into stock_scores table.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    run_date = date.today().isoformat()

    cursor.execute("""
        SELECT
            id,
            strategy,
            current_price,
            pe,
            qtr_sales_var_pct,
            qtr_profit_var_pct,
            roce_pct,
            dma_50,
            dma_200,
            market_cap
        FROM stocks
    """)

    rows = cursor.fetchall()
    print(f"📊 Found {len(rows)} stocks to score")

    scored = 0

    for row in rows:
        stock = dict(row)
        stock_id = stock["id"]
        strategy = stock["strategy"]

        if not stock_id or not strategy:
            continue

        score = composite_score(stock)

        cursor.execute("""
            INSERT INTO stock_scores (
                stock_id,
                strategy,
                composite_score,
                run_date
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(stock_id, strategy)
            DO UPDATE SET
                composite_score = excluded.composite_score,
                run_date = excluded.run_date
        """, (
            stock_id,
            strategy,
            score,
            run_date
        ))

        scored += 1

    conn.commit()
    conn.close()

    print(f"✅ Composite score assigned to {scored} stocks")


if __name__ == "__main__":
    score_all_stocks()
