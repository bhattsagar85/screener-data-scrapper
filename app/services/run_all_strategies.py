from app.services.run_strategy_pipeline import run_strategy
from app.strategy.api_registry import STRATEGIES


def run_all_strategies():
    """
    Run full pipeline for ALL strategies.
    """
    results = []

    for strategy_number, meta in STRATEGIES.items():
        try:
            result = run_strategy(strategy_number)
            results.append({
                "strategy_number": strategy_number,
                "strategy": meta["key"],
                "label": meta["label"],
                "status": "success",
                "stocks_fetched": result.get("stocks_fetched", 0),
            })
        except Exception as e:
            results.append({
                "strategy_number": strategy_number,
                "strategy": meta["key"],
                "label": meta["label"],
                "status": "failed",
                "error": str(e),
            })

    return {
        "total_strategies": len(STRATEGIES),
        "results": results,
    }
