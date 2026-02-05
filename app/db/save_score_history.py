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
            sc.stock_id,
            s.company,
            sc.strategy,
            sc.composite_score
        FROM stock_scores sc
        JOIN stocks s ON s.id = sc.stock_id
        WHERE sc.composite_score IS NOT NULL
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
                run_date
            )
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(stock_id, run_date)
            DO UPDATE SET
                composite_score = excluded.composite_score
        """, (
            row["stock_id"],
            row["company"],
            row["strategy"],
            row["composite_score"],
            run_date
        ))

    conn.commit()
    conn.close()

    print("✅ Score history deduplicated & saved")


if __name__ == "__main__":
    save_score_history()
