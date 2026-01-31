STRATEGIES = {

    # -------------------------------------------------
    # 1️⃣ Core Quality + Trend (Institutional Momentum)
    # -------------------------------------------------
    "quality_golden_cross": {
        "label": "Institutional Golden Cross (Quality + Trend)",
        "query": (
            "Return on capital employed > 22 "
            "AND Current price > DMA 50 "
            "AND DMA 50 > DMA 200 "
            "AND Promoter holding > 45"
        ),
    },

    # -------------------------------------------------
    # 2️⃣ High Quality Compounders (Wealth Creation)
    # -------------------------------------------------
    "quality_compounders": {
        "label": "High Quality Compounders (2026 Edition)",
        "query": (
            "Return on capital employed > 25 "
            "AND Market Capitalization > 5000 "
            "AND Sales growth 5Years > 15 "
            "AND Debt to equity < 0.2"
        ),
    },

    # -------------------------------------------------
    # 3️⃣ Value + Quality (PM's Alpha)
    # -------------------------------------------------
    "gold_standard_pm": {
        "label": "Portfolio Manager's Gold Standard",
        "query": (
            "Return on capital employed > 22 "
            "AND Debt to equity < 0.3 "
            "AND Sales growth 5Years > 18 "
            "AND Profit growth 5Years > 18 "
            "AND Piotroski score > 7 "
            "AND Promoter holding > 40"
        ),
    },

    # -------------------------------------------------
    # 4️⃣ Large & Stable Leaders
    # -------------------------------------------------
    "largecap_quality": {
        "label": "Largecap Quality Leaders",
        "query": (
            "Market Capitalization > 50000 "
            "AND Return on capital employed > 20 "
            "AND Dividend yield > 1"
        ),
    },

    # -------------------------------------------------
    # 5️⃣ Midcap Quality Growth (Alpha Hunt)
    # -------------------------------------------------
    "midcap_quality_growth": {
        "label": "Midcap Growth Sieve",
        "query": (
            "Market Capitalization > 2000 "
            "AND Market Capitalization < 25000 "
            "AND Return on capital employed > 20 "
            "AND Sales growth 3Years > 20 "
            "AND Current price > DMA 50"
        ),
    },

    # -------------------------------------------------
    # 6️⃣ Cash-Rich, Debt-Free Businesses
    # -------------------------------------------------
    "debt_free_cash_generators": {
        "label": "Cash Flow Kings (Debt-Free)",
        "query": (
            "Debt to equity = 0 "
            "AND Return on capital employed > 20 "
            "AND Operating cash flow 3years > 0"
        ),
    },

    # -------------------------------------------------
    # 7️⃣ Consistent Earnings Machines
    # -------------------------------------------------
    "consistent_earnings": {
        "label": "High-Conviction Consistency",
        "query": (
            "Sales growth 5Years > 15 "
            "AND Profit growth 5Years > 15 "
            "AND ROE 5Years > 20"
        ),
    },

    # -------------------------------------------------
    # 8️⃣ Quality Growth at Reasonable Price (Sweet Spot)
    # -------------------------------------------------
    "qgarp_valuation": {
        "label": "Quality Growth at Reasonable Price (QGARP)",
        "query": (
            "Return on capital employed > 20 "
            "AND Sales growth 5Years > 15 "
            "AND PEG Ratio < 1.2 "
            "AND PE < 35"
        ),
    },

    # -------------------------------------------------
    # 9️⃣ Graham Defensive (Deep Value)
    # -------------------------------------------------
    "graham_defensive": {
        "label": "Value Discovery (High Quality Deep Value)",
        "query": (
            "Price to Earning < 18 "
            "AND Price to book value < 2.5 "
            "AND Debt to equity < 0.5 "
            "AND Return on capital employed > 15"
        ),
    },

    # -------------------------------------------------
    # 🔟 Financial Fortress (Piotroski Focus)
    # -------------------------------------------------
    "financial_fortress": {
        "label": "Piotroski 8+ Fortress",
        "query": (
            "Piotroski score > 7 "
            "AND Return on capital employed > 18 "
            "AND Debt to equity < 0.4 "
            "AND Net profit margin > 10"
        ),
    },

    # -------------------------------------------------
    # 1️⃣1️⃣ Free Cash Flow Yield Efficiency
    # -------------------------------------------------
    "fcf_yield_efficiency": {
        "label": "Free Cash Flow Compounders",
        "query": (
            "Price to Free Cash Flow < 25 "
            "AND Free cash flow 5years > 0 "
            "AND Return on capital employed > 20"
        ),
    },

    # -------------------------------------------------
    # 1️⃣2️⃣ Magic Formula (Enhanced)
    # -------------------------------------------------
    "magic_formula_india": {
        "label": "Enhanced Magic Formula",
        "query": (
            "Earnings yield > 12 "
            "AND Return on capital employed > 22 "
            "AND Debt to equity < 0.3 "
            "AND Sales growth 3Years > 12"
        ),
    },

}