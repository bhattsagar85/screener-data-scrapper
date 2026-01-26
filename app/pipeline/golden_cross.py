from app.tools.screener_browser import ScreenerBrowser
from app.tools.screener_extractor import ScreenerExtractor
from app.services.column_mapper import normalize_row
from app.validators.golden_cross import is_golden_cross


def run_golden_cross_scan():
    """
    End-to-end Golden Cross screener pipeline.
    Can be called from API, CLI, cron, tests, etc.
    """

    browser = ScreenerBrowser(headless=True)
    extractor = ScreenerExtractor()

    html = browser.run_query(
        "Current price > DMA 50 AND DMA 50 > DMA 200"
    )

    raw_rows = extractor.extract(html)
    normalized = [normalize_row(r) for r in raw_rows]

    validated = [
        stock for stock in normalized
        if is_golden_cross(stock)
    ]

    return {
        "total_screened": len(normalized),
        "golden_cross_count": len(validated),
        "stocks": validated,
    }
