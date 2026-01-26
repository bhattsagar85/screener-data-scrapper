from app.tools.screener_browser import ScreenerBrowser
from app.tools.screener_extractor import ScreenerExtractor
from app.services.column_mapper import normalize_row
from app.validators.golden_cross import is_golden_cross
from app.strategy.registery import STRATEGIES
from app.db.insert import insert_stocks


def choose_strategy():
    print("\n📊 Available Screeners\n")
    keys = list(STRATEGIES.keys())

    for i, key in enumerate(keys, start=1):
        print(f"{i}. {STRATEGIES[key]['label']}")

    choice = input("\nSelect a screener (number): ").strip()

    if not choice.isdigit():
        raise ValueError("Invalid input")

    idx = int(choice) - 1
    if idx < 0 or idx >= len(keys):
        raise ValueError("Invalid choice")

    key = keys[idx]
    return key, STRATEGIES[key]


def choose_display_limit(total):
    print("\n📄 How many stocks do you want to see?")
    print("1. Show top 10")
    print("2. Show top 20")
    print("3. Show ALL")

    choice = input("Choose (1/2/3): ").strip()

    if choice == "1":
        return min(10, total)
    elif choice == "2":
        return min(20, total)
    elif choice == "3":
        return total
    else:
        return min(10, total)


def main():
    print("\n🚀 Screener Runner")

    strategy_key, strategy = choose_strategy()

    print("\n▶ Running:", strategy["label"])
    print("Query:", strategy["query"])
    print("-" * 60)

    browser = ScreenerBrowser(headless=False)
    extractor = ScreenerExtractor()

    html = browser.run_query(strategy["query"])

    rows = extractor.extract(html)
    stocks = [normalize_row(r) for r in rows]

    print(f"✅ Total stocks fetched: {len(stocks)}")

    # Optional validation
    if "DMA 50 > DMA 200" in strategy["query"]:
        print("⭐ Golden Cross enforced by Screener query")

    # 💾 SAVE TO DATABASE
    insert_stocks(stocks, strategy=strategy_key)

    limit = choose_display_limit(len(stocks))

    print("-" * 60)

    for stock in stocks[:limit]:
        print(
            f"{stock['company']:<25} | "
            f"Price: {stock['current_price']:>8} | "
            f"ROCE: {stock['roce_pct']:>6}"
        )

    print("-" * 60)
    print("✅ Done.\n")


if __name__ == "__main__":
    main()
