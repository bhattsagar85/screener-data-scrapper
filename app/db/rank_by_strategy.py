import sqlite3
from pathlib import Path

# Absolute DB path
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def rank_stocks_per_strategy(top_n: int | None = None):
    """
    Rank stocks by composite_score within each strategy.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get distinct strategies
    cursor.execute("""
        SELECT DISTINCT strategy
        FROM stocks
        WHERE composite_score IS NOT NULL
    """)
    strategies = [row["strategy"] for row in cursor.fetchall()]

    if not strategies:
        print("❌ No strategies found")
        return

    for strategy in strategies:
        print("\n" + "=" * 70)
        print(f"📌 Strategy: {strategy}")
        print("=" * 70)

        query = """
            SELECT
                company,
                composite_score,
                roce_pct,
                pe,
                current_price
            FROM stocks
            WHERE strategy = ?
            ORDER BY composite_score DESC
        """

        if top_n:
            query += " LIMIT ?"
            cursor.execute(query, (strategy, top_n))
        else:
            cursor.execute(query, (strategy,))

        rows = cursor.fetchall()

        for idx, row in enumerate(rows, start=1):
            print(
                f"{idx:>2}. "
                f"{row['company']:<25} | "
                f"Score: {row['composite_score']:>6.2f} | "
                f"ROCE: {row['roce_pct']:>6} | "
                f"PE: {row['pe']:>6}"
            )

    conn.close()


if __name__ == "__main__":
    # Change this number if you want top 5 / top 20 etc.
    rank_stocks_per_strategy(top_n=10)
