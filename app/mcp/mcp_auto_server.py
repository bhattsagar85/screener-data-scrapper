import os
import logging
from typing import Any, Dict

# 🔇 Silence EVERYTHING
logging.disable(logging.CRITICAL)
os.environ["HTTPX_LOG_LEVEL"] = "none"

import httpx
from mcp.server.fastmcp import FastMCP

FASTAPI_BASE_URL = "http://127.0.0.1:8000"
OPENAPI_URL = f"{FASTAPI_BASE_URL}/openapi.json"

mcp = FastMCP("Screener Agent MCP Server")


def load_openapi() -> Dict[str, Any]:
    # No prints, no logs, no stderr
    with httpx.Client() as client:
        r = client.get(OPENAPI_URL)
        r.raise_for_status()
        return r.json()


def register_openapi_tools():
    openapi = load_openapi()
    paths = openapi.get("paths", {})

    for path, methods in paths.items():
        for method, spec in methods.items():
            operation_id = spec.get("operationId")
            if not operation_id:
                continue

            summary = spec.get("summary", "")
            description = spec.get("description", "")

            def make_tool(path=path, method=method):
                def tool(**kwargs):
                    url = f"{FASTAPI_BASE_URL}{path}"
                    if method.upper() == "GET":
                        r = httpx.get(url, params=kwargs)
                    else:
                        r = httpx.request(method.upper(), url, json=kwargs)
                    r.raise_for_status()
                    return r.json()

                return tool

            mcp.tool(
                name=operation_id,
                description=f"{summary}\n\n{description}".strip(),
            )(make_tool)


# ✅ Register tools BEFORE run()
register_openapi_tools()

if __name__ == "__main__":
    # 🚨 Nothing else must write to stdout
    mcp.run()
