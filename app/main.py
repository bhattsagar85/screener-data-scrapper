from fastapi import FastAPI, HTTPException
from app.pipeline.golden_cross import run_golden_cross_scan
from pydantic import BaseModel

from app.services.run_all_strategies import run_all_strategies
from app.services.portfolio_read_service import get_latest_portfolio
from app.services.run_strategy_pipeline import run_strategy
from app.strategy.api_registry import STRATEGIES
from app.services.portfolio_service import build_and_fetch_portfolio


app = FastAPI(title="Screener Agent API")


class StrategyRequest(BaseModel):
    strategy_number: int
    top_n: int = 10

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/screen/golden-cross")
def golden_cross_screen():
    """
    Trigger Golden Cross screening.
    """
    return run_golden_cross_scan()

@app.get(
    "/strategies",
    summary="List available stock screening strategies",
    description=(
        "Returns all supported stock screening strategies. "
        "Agents should call this first to understand which strategies exist "
        "before requesting portfolios or running calculations."
    ),
)
def list_strategies():
    return {
        k: {
            "label": v["label"],
            "query": v["query"]
        }
        for k, v in STRATEGIES.items()
    }


@app.post(
    "/run",
    summary="Run full screening pipeline for one strategy",
    description=(
        "Runs the complete screening pipeline: Screener query, data extraction, "
        "scoring, decay, ranking, and history storage. "
        "This is a heavy operation and should be used sparingly."
    ),
)
def run_strategy_api(req: StrategyRequest):
    try:
        result = run_strategy(req.strategy_number)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/portfolio/build",
    summary="Build top-N portfolio for a strategy",
    description=(
        "Builds a ranked portfolio of top N stocks for a given strategy "
        "using the latest decayed scores. Writes results to database."
    ),
)
def build_portfolio_api(req: StrategyRequest):
    try:
        return build_and_fetch_portfolio(
            strategy_number=req.strategy_number,
            top_n=req.top_n,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 


@app.get(
    "/portfolio/latest",
    summary="Fetch latest ranked portfolio for a strategy",
    description=(
        "Returns the most recently built portfolio for a strategy. "
        "This endpoint is fast, read-only, and safe for frequent agent usage. "
        "Agents should prefer this endpoint for analysis and recommendations."
    ),
)
def portfolio_latest(strategy_number: int):
    try:
        return get_latest_portfolio(strategy_number)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/run-all",
    summary="Run full screening pipeline for ALL strategies",
    description=(
        "Runs all screening strategies sequentially. "
        "Intended for scheduled (cron) usage, not frequent agent calls."
    ),
)
def run_all_api():
    try:
        return run_all_strategies()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))                           
