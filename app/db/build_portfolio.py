import sqlite3
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "screener.db"


def build_portfolio(strategy: str, top_n: int = 10):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    run_date = date.today().isoformat()

    # 🔍 Debug: check if strategy exists
    cursor.execute("""
        SELECT COUNT(*) FROM stocks WHERE strategy = ?
    """, (strategy,))
    total = cursor.fetchone()[0]

    if total == 0:
        print(f"❌ Strategy '{strategy}' not found in stocks table")
        conn.close()
        return

    # 🔍 Debug: check if scores exist (source of truth: stock_scores)
    cursor.execute("""
        SELECT COUNT(*) FROM stock_scores
        WHERE strategy = ?
          AND decayed_score IS NOT NULL
          AND strategy_rank IS NOT NULL
    """, (strategy,))
    valid = cursor.fetchone()[0]

    if valid == 0:
        print(f"❌ No ranked stocks for strategy '{strategy}' (scores missing)")
        conn.close()
        return

    # ✅ Fetch top N
    cursor.execute("""
        SELECT
            s.company,
            sc.strategy_rank,
            sc.decayed_score
        FROM stock_scores sc
        JOIN stocks s ON s.id = sc.stock_id
        WHERE sc.strategy = ?
          AND sc.decayed_score IS NOT NULL
          AND sc.strategy_rank IS NOT NULL
        ORDER BY sc.strategy_rank ASC
        LIMIT ?
    """, (strategy, top_n))

    rows = cursor.fetchall()

    for row in rows:
        cursor.execute("""
            INSERT INTO portfolios (
                strategy,
                company,
                strategy_rank,
                decayed_score,
                run_date
            ) VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(strategy, company, run_date) DO UPDATE SET
                strategy_rank = excluded.strategy_rank,
                decayed_score = excluded.decayed_score
        """, (
            strategy,
            row["company"],
            row["strategy_rank"],
            row["decayed_score"],
            run_date
        ))

    conn.commit()
    conn.close()

    print(f"📦 Portfolio built: {strategy} (Top {len(rows)})")
