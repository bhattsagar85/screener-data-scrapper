import sqlite3
from pathlib import Path

# Absolute DB path
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def update_strategy_ranks():
    """
    Rank stocks per strategy using decayed_score.
    Source of truth: stock_scores table.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch strategies that have decayed scores
    cursor.execute("""
        SELECT DISTINCT strategy
        FROM stock_scores
        WHERE decayed_score IS NOT NULL
    """)
    strategies = [row["strategy"] for row in cursor.fetchall()]

    if not strategies:
        print("❌ No strategies with decayed scores found")
        conn.close()
        return

    for strategy in strategies:
        cursor.execute("""
            WITH ranked AS (
                SELECT
                    stock_id,
                    ROW_NUMBER() OVER (
                        ORDER BY decayed_score DESC
                    ) AS strategy_rank
                FROM stock_scores
                WHERE strategy = ?
                  AND decayed_score IS NOT NULL
            )
            UPDATE stock_scores
            SET strategy_rank = (
                SELECT strategy_rank
                FROM ranked
                WHERE ranked.stock_id = stock_scores.stock_id
            )
            WHERE strategy = ?
        """, (strategy, strategy))

        print(f"✅ Ranked strategy: {strategy}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    update_strategy_ranks()
