"""
Composite Scoring Module (v3)

Includes:
- Quality
- Growth
- Valuation
- Trend
- Market Cap Stability
- Liquidity Penalty (market cap proxy)
"""


def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    return max(min_val, min(value, max_val))


# -------------------------------------------------
# 1️⃣ Quality Score (ROCE)
# -------------------------------------------------

def quality_score(roce):
    try:
        roce = float(roce)
    except Exception:
        return 0.0

    if roce < 10:
        return 0
    elif roce < 15:
        return 30
    elif roce < 20:
        return 60
    elif roce < 25:
        return 80
    else:
        return 100


# -------------------------------------------------
# 2️⃣ Growth Score
# -------------------------------------------------

def _growth_component(value):
    try:
        value = float(value)
    except Exception:
        return None

    if value < 0:
        return 0
    elif value < 10:
        return 30
    elif value < 20:
        return 60
    else:
        return 100


def growth_score(qtr_sales_var_pct, qtr_profit_var_pct):
    scores = []

    s = _growth_component(qtr_sales_var_pct)
    p = _growth_component(qtr_profit_var_pct)

    if s is not None:
        scores.append(s)
    if p is not None:
        scores.append(p)

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


# -------------------------------------------------
# 3️⃣ Valuation Score
# -------------------------------------------------

def valuation_score(pe):
    try:
        pe = float(pe)
    except Exception:
        return 50.0

    if pe < 8:
        return 60
    elif pe <= 15:
        return 100
    elif pe <= 25:
        return 70
    else:
        return 30


# -------------------------------------------------
# 4️⃣ Trend Score
# -------------------------------------------------

def trend_score(current_price, dma_50, dma_200):
    try:
        price = float(current_price)
        d50 = float(dma_50)
        d200 = float(dma_200)
    except Exception:
        return 0.0

    if price > d50 > d200:
        return 100
    elif price > d200:
        return 70
    else:
        return 0


# -------------------------------------------------
# 5️⃣ Market Cap Stability Score
# -------------------------------------------------

def market_cap_score(market_cap):
    try:
        mc = float(market_cap)
    except Exception:
        return 0.0

    if mc < 300:
        return 10
    elif mc < 1000:
        return 30
    elif mc < 5000:
        return 60
    elif mc < 20000:
        return 85
    else:
        return 100


# -------------------------------------------------
# 6️⃣ Liquidity Penalty (NEW)
# -------------------------------------------------

def liquidity_penalty(market_cap):
    try:
        mc = float(market_cap)
    except Exception:
        return 20  # harsh penalty if missing

    if mc < 300:
        return 20
    elif mc < 1000:
        return 10
    elif mc < 5000:
        return 5
    else:
        return 0


# -------------------------------------------------
# 🧮 Final Composite Score
# -------------------------------------------------

def composite_score(stock: dict) -> float:
    q = quality_score(stock.get("roce_pct"))
    g = growth_score(
        stock.get("qtr_sales_var_pct"),
        stock.get("qtr_profit_var_pct"),
    )
    v = valuation_score(stock.get("pe"))
    t = trend_score(
        stock.get("current_price"),
        stock.get("dma_50"),
        stock.get("dma_200"),
    )
    m = market_cap_score(stock.get("market_cap"))

    base_score = (
        0.35 * q +
        0.20 * g +
        0.20 * v +
        0.15 * t +
        0.10 * m
    )

    penalty = liquidity_penalty(stock.get("market_cap"))

    final_score = base_score - penalty

    return round(clamp(final_score), 2)
