import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def update_strategy_ranks():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all strategies present
    cursor.execute("""
        SELECT DISTINCT strategy
        FROM stocks
        WHERE decayed_score IS NOT NULL
    """)
    strategies = [row["strategy"] for row in cursor.fetchall()]

    for strategy in strategies:
        cursor.execute(f"""
            WITH ranked AS (
                SELECT
                    id,
                    ROW_NUMBER() OVER (
                        ORDER BY decayed_score DESC
                    ) AS rank
                FROM stocks
                WHERE strategy = ?
            )
            UPDATE stocks
            SET strategy_rank = (
                SELECT rank FROM ranked WHERE ranked.id = stocks.id
            )
            WHERE strategy = ?
        """, (strategy, strategy))

        print(f"✅ Ranked strategy: {strategy}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    update_strategy_ranks()
