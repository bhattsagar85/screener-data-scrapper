import requests
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8000"


class ScreenerMCPClient:
    """
    Lightweight MCP-compatible client for Screener Agent API.
    """

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    # ---------------------------------------------------------
    # 🔍 DISCOVERY
    # ---------------------------------------------------------

    def list_strategies(self) -> Dict[str, Any]:
        resp = requests.get(f"{self.base_url}/strategies")
        resp.raise_for_status()
        return resp.json()

    # ---------------------------------------------------------
    # 🚀 HEAVY OPERATIONS (ADMIN / SCHEDULER)
    # ---------------------------------------------------------

    def run_all_strategies(self) -> Dict[str, Any]:
        """
        Run full pipeline for ALL strategies.
        """
        resp = requests.post(f"{self.base_url}/run-all")
        resp.raise_for_status()
        return resp.json()

    def run_strategy(
        self,
        strategy_number: int,
        top_n: int = 10,
    ) -> Dict[str, Any]:
        """
        Run full pipeline for a SINGLE strategy.

        Includes:
        - Screener fetch
        - Scoring
        - Decay
        - Ranking
        - (Optional) Portfolio build
        """
        payload = {
            "strategy_number": strategy_number,
            "top_n": top_n,
        }

        resp = requests.post(
            f"{self.base_url}/run",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()

    def build_portfolio(
        self,
        strategy_number: int,
        top_n: int = 10,
    ) -> Dict[str, Any]:
        payload = {
            "strategy_number": strategy_number,
            "top_n": top_n,
        }

        resp = requests.post(
            f"{self.base_url}/portfolio/build",
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()

    # ---------------------------------------------------------
    # 📊 SAFE READ APIs (AGENT-FRIENDLY)
    # ---------------------------------------------------------

    def get_latest_portfolio(self, strategy_number: int) -> Dict[str, Any]:
        resp = requests.get(
            f"{self.base_url}/portfolio/latest",
            params={"strategy_number": strategy_number},
        )
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------
# 🧪 EXAMPLE USAGE
# ---------------------------------------------------------

if __name__ == "__main__":
    client = ScreenerMCPClient()

    # 1️⃣ Discover strategies
    strategies = client.list_strategies()
    print("\n📊 Available Strategies")
    for k, v in strategies.items():
        print(f"{k}. {v['label']}")

    # 2️⃣ Run ONE strategy (example: strategy 7)
    print("\n🚀 Running single strategy")
    run_result = client.run_strategy(strategy_number=7, top_n=10)
    print(run_result)

    # 3️⃣ Fetch latest portfolio
    portfolio = client.get_latest_portfolio(strategy_number=7)
    print("\n📈 Latest Portfolio")
    print(portfolio)
