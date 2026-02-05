from fastapi import APIRouter, Query
import sqlite3
from app.strategy.api_registry import STRATEGIES

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio Analysis"]
)

@router.get(
    "/analysis",
    summary="Detailed portfolio analysis view",
    description=(
        "Returns detailed fundamentals and decayed scores for the latest "
        "ranked stocks of a given strategy."
    ),
)
def portfolio_analysis(
    strategy_number: int = Query(..., description="Strategy number from /strategies")
):
    if strategy_number not in STRATEGIES:
        return {"error": "Invalid strategy number"}

    strategy_key = STRATEGIES[strategy_number]["key"]

    conn = sqlite3.connect("data/screener.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            sc.strategy_rank AS rank,
            s.company,
            s.symbol,
            sc.decayed_score,

            s.current_price AS cmp,
            s.pe,
            s.market_cap,
            s.dividend_yield,
            s.net_profit_qtr,
            s.qtr_profit_var_pct,
            s.sales_qtr_rs_cr,
            s.qtr_sales_var_pct,
            s.roce_pct

        FROM stock_scores sc
        JOIN stocks s ON s.id = sc.stock_id
        WHERE sc.strategy = ?
          AND sc.strategy_rank IS NOT NULL
        ORDER BY sc.strategy_rank ASC
        """,
        (strategy_key,),
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        return {
            "strategy": strategy_key,
            "count": 0,
            "message": "No ranked stocks found. Run /run or /run-all first."
        }

    return {
        "strategy": strategy_key,
        "count": len(rows),
        "stocks": [
            {
                "rank": r["rank"],
                "company": r["company"],
                "symbol": r["symbol"],
                "decayed_score": r["decayed_score"],

                "cmp": r["cmp"],
                "pe": r["pe"],
                "market_cap": r["market_cap"],
                "dividend_yield": r["dividend_yield"],
                "net_profit_qtr": r["net_profit_qtr"],
                "qtr_profit_var_pct": r["qtr_profit_var_pct"],
                "sales_qtr": r["sales_qtr_rs_cr"],
                "qtr_sales_var_pct": r["qtr_sales_var_pct"],
                "roce": r["roce_pct"],
            }
            for r in rows
        ]
    }
