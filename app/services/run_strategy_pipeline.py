import time

from app.tools.screener_browser import ScreenerBrowser
from app.tools.screener_extractor import ScreenerExtractor
from app.services.column_mapper import normalize_row
from app.db.insert import insert_stocks
from app.db.score_stocks import score_all_stocks
from app.db.apply_score_decay import apply_score_decay
from app.db.update_strategy_rank import update_strategy_ranks
from app.db.save_score_history import save_score_history
from app.strategy.api_registry import STRATEGIES
from playwright.sync_api import TimeoutError


def run_strategy(strategy_number: int) -> dict:
    """
    Run full pipeline for a single strategy with:
    - visible browser (headless=False)
    - retry logic
    - safe selector handling
    """

    if strategy_number not in STRATEGIES:
        raise ValueError("Invalid strategy number")

    strategy = STRATEGIES[strategy_number]
    strategy_key = strategy["key"]
    query = strategy["query"]

    print(f"\n🚀 Running strategy: {strategy_key}")

    # 🔍 HEADLESS DISABLED FOR DEBUGGING
    browser = ScreenerBrowser(headless=False)
    extractor = ScreenerExtractor()

    # --------------------------------------------------
    # 1️⃣ Run Screener (with retry)
    # --------------------------------------------------
    max_attempts = 2
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"🌐 Screener attempt {attempt} for {strategy_key}")
            html = browser.run_query(query)
            break
        except TimeoutError as e:
            last_error = e
            print(f"⚠️ Timeout on attempt {attempt} for {strategy_key}")
            time.sleep(5)
        except Exception as e:
            last_error = e
            print(f"❌ Error on attempt {attempt} for {strategy_key}: {e}")
            time.sleep(5)
    else:
        raise last_error

    # --------------------------------------------------
    # 2️⃣ Extract + normalize
    # --------------------------------------------------
    rows = extractor.extract(html)
    stocks = [normalize_row(r) for r in rows]

    print(f"📊 Extracted {len(stocks)} stocks for {strategy_key}")

    if not stocks:
        raise RuntimeError(f"No stocks extracted for strategy '{strategy_key}'")

    # --------------------------------------------------
    # 3️⃣ Save / upsert stocks
    # --------------------------------------------------
    insert_stocks(stocks, strategy=strategy_key)

    # --------------------------------------------------
    # 4️⃣ Compute scores
    # --------------------------------------------------
    score_all_stocks()

    # --------------------------------------------------
    # 5️⃣ Apply score decay
    # --------------------------------------------------
    apply_score_decay()

    # --------------------------------------------------
    # 6️⃣ Rank using decayed_score
    # --------------------------------------------------
    update_strategy_ranks()

    # --------------------------------------------------
    # 7️⃣ Save score history snapshot
    # --------------------------------------------------
    save_score_history()

    print(f"✅ Strategy completed: {strategy_key}")

    # Polite delay (important for run-all)
    time.sleep(3)

    return {
        "strategy": strategy_key,
        "label": strategy["label"],
        "stocks_fetched": len(stocks),
        "status": "completed",
    }
