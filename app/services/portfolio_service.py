from app.db.build_portfolio import build_portfolio
from app.strategy.api_registry import STRATEGIES
import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def build_and_fetch_portfolio(strategy_number: int, top_n: int = 10):
    if strategy_number not in STRATEGIES:
        raise ValueError("Invalid strategy number")

    strategy = STRATEGIES[strategy_number]
    strategy_key = strategy["key"]
    run_date = date.today().isoformat()

    # 1️⃣ Build / update portfolio
    build_portfolio(strategy_key, top_n)

    # 2️⃣ Fetch portfolio rows
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            company,
            strategy_rank,
            decayed_score
        FROM portfolios
        WHERE strategy = ?
          AND run_date = ?
        ORDER BY strategy_rank ASC
    """, (strategy_key, run_date))

    rows = cursor.fetchall()
    conn.close()

    return {
        "strategy": strategy_key,
        "label": strategy["label"],
        "top_n": top_n,
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
