import sqlite3
from pathlib import Path

from app.scoring.composite_score import composite_score

# Absolute DB path (important)
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def score_all_stocks():
    """
    Compute composite score for all stocks
    and update the database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch all stocks
    cursor.execute("""
        SELECT
            id,
            current_price,
            pe,
            qtr_sales_var_pct,
            qtr_profit_var_pct,
            roce_pct,
            dma_50,
            dma_200
        FROM stocks
    """)

    rows = cursor.fetchall()
    print(f"📊 Found {len(rows)} stocks to score")

    updated = 0

    for row in rows:
        stock = dict(row)

        score = composite_score(stock)

        cursor.execute(
            """
            UPDATE stocks
            SET composite_score = ?
            WHERE id = ?
            """,
            (score, stock["id"]),
        )

        updated += 1

    conn.commit()
    conn.close()

    print(f"✅ Composite score assigned to {updated} stocks")


if __name__ == "__main__":
    score_all_stocks()
