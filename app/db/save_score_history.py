import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def save_score_history():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    run_date = date.today().isoformat()

    cursor.execute("""
        SELECT
            id,
            company,
            strategy,
            composite_score,
            decayed_score,
            strategy_rank
        FROM stocks
        WHERE composite_score IS NOT NULL
    """)

    rows = cursor.fetchall()
    print(f"📸 Saving score history for {len(rows)} stocks")

    for row in rows:
        cursor.execute("""
            INSERT INTO stock_score_history (
                stock_id,
                company,
                strategy,
                composite_score,
                strategy_rank,
                run_date
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(stock_id, run_date) DO UPDATE SET
                composite_score = excluded.composite_score,
                strategy_rank = excluded.strategy_rank
        """, (
            row["id"],
            row["company"],
            row["strategy"],
            row["composite_score"],
            row["strategy_rank"],
            run_date
        ))

    conn.commit()
    conn.close()

    print("✅ Score history deduplicated & saved")


if __name__ == "__main__":
    save_score_history()
