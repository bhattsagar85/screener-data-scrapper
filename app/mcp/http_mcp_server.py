from mcp.server.fastmcp import FastMCP
import httpx

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

mcp = FastMCP(
    name="Screener Agent MCP",
    transport="http",
    host="127.0.0.1",
    port=9001,
)


@mcp.tool(
    name="get_latest_portfolio",
    description="Fetch latest ranked portfolio for a given strategy number."
)
def get_latest_portfolio(strategy_number: int):
    r = httpx.get(
        f"{FASTAPI_BASE_URL}/portfolio/latest",
        params={"strategy_number": strategy_number},
    )
    r.raise_for_status()
    return r.json()


@mcp.tool(
    name="list_strategies",
    description="List all available screening strategies."
)
def list_strategies():
    r = httpx.get(f"{FASTAPI_BASE_URL}/strategies")
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    mcp.run()
