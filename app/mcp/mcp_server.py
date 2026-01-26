import httpx
from mcp.server.fastmcp import FastMCP

API_BASE = "http://127.0.0.1:8000"

mcp = FastMCP("Stock Screener Intelligence")

# -----------------------------------------
# Tool 1: List Strategies
# -----------------------------------------
@mcp.tool()
def list_strategies() -> dict:
    """
    Get all available screening strategies.
    """
    r = httpx.get(f"{API_BASE}/strategies")
    r.raise_for_status()
    return r.json()


# -----------------------------------------
# Tool 2: Get Latest Portfolio
# -----------------------------------------
@mcp.tool()
def get_latest_portfolio(strategy_number: int) -> dict:
    """
    Fetch latest ranked portfolio for a strategy.
    """
    r = httpx.get(
        f"{API_BASE}/portfolio/latest",
        params={"strategy_number": strategy_number},
    )
    r.raise_for_status()
    return r.json()


# -----------------------------------------
# Tool 3: Run Single Strategy (Heavy)
# -----------------------------------------
@mcp.tool()
def run_strategy(strategy_number: int) -> dict:
    """
    Run full pipeline for one strategy (slow).
    """
    r = httpx.post(
        f"{API_BASE}/run",
        json={"strategy_number": strategy_number},
        timeout=600,
    )
    r.raise_for_status()
    return r.json()


# -----------------------------------------
# Tool 4: Run All Strategies (Batch)
# -----------------------------------------
@mcp.tool()
def run_all_strategies() -> dict:
    """
    Run all strategies (very slow, scheduled).
    """
    r = httpx.post(f"{API_BASE}/run-all", timeout=1200)
    r.raise_for_status()
    return r.json()


# -----------------------------------------
# Tool 5: Build Portfolio
# -----------------------------------------
@mcp.tool()
def build_portfolio(strategy_number: int, top_n: int = 10) -> dict:
    """
    Build top-N portfolio for a strategy.
    """
    r = httpx.post(
        f"{API_BASE}/portfolio/build",
        json={"strategy_number": strategy_number, "top_n": top_n},
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    mcp.run()
