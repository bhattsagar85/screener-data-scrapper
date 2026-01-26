import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


DECAY_WEIGHTS = [0.6, 0.3, 0.1]  # most recent → oldest


def compute_decayed_score(scores: list[float]) -> float:
    """
    Compute weighted decayed score from historical scores.
    """
    weights = DECAY_WEIGHTS[: len(scores)]
    total_weight = sum(weights)

    weighted_sum = sum(s * w for s, w in zip(scores, weights))
    return round(weighted_sum / total_weight, 2)


def apply_score_decay():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch distinct stocks with history
    cursor.execute("""
        SELECT DISTINCT stock_id
        FROM stock_score_history
    """)
    stock_ids = [row["stock_id"] for row in cursor.fetchall()]

    print(f"📉 Applying score decay to {len(stock_ids)} stocks")

    updated = 0

    for stock_id in stock_ids:
        cursor.execute("""
            SELECT composite_score
            FROM stock_score_history
            WHERE stock_id = ?
            ORDER BY run_date DESC
            LIMIT 3
        """, (stock_id,))

        rows = cursor.fetchall()
        scores = [row["composite_score"] for row in rows]

        if not scores:
            continue

        decayed = compute_decayed_score(scores)

        cursor.execute("""
            UPDATE stocks
            SET decayed_score = ?
            WHERE id = ?
        """, (decayed, stock_id))

        updated += 1

    conn.commit()
    conn.close()

    print(f"✅ Decayed score updated for {updated} stocks")


if __name__ == "__main__":
    apply_score_decay()
