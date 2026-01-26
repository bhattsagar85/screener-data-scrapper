import sqlite3
from pathlib import Path
from app.strategy.api_registry import STRATEGIES

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def get_latest_portfolio(strategy_number: int):
    if strategy_number not in STRATEGIES:
        raise ValueError("Invalid strategy number")

    strategy = STRATEGIES[strategy_number]
    strategy_key = strategy["key"]

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 🔹 Find latest run_date for this strategy
    cursor.execute("""
        SELECT MAX(run_date) AS latest_date
        FROM portfolios
        WHERE strategy = ?
    """, (strategy_key,))
    row = cursor.fetchone()

    if not row or not row["latest_date"]:
        conn.close()
        return {
            "strategy": strategy_key,
            "label": strategy["label"],
            "count": 0,
            "portfolio": [],
            "message": "No portfolio found. Run /portfolio/build first."
        }

    latest_date = row["latest_date"]

    # 🔹 Fetch portfolio rows
    cursor.execute("""
        SELECT
            company,
            strategy_rank,
            decayed_score
        FROM portfolios
        WHERE strategy = ?
          AND run_date = ?
        ORDER BY strategy_rank ASC
    """, (strategy_key, latest_date))

    rows = cursor.fetchall()
    conn.close()

    return {
        "strategy": strategy_key,
        "label": strategy["label"],
        "run_date": latest_date,
        "count": len(rows),
        "portfolio": [
            {
                "rank": r["strategy_rank"],
                "company": r["company"],
                "decayed_score": round(r["decayed_score"], 2),
            }
            for r in rows
        ],
    }
