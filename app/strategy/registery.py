STRATEGIES = {

    # -------------------------------------------------
    # 1️⃣ Core Quality + Trend
    # -------------------------------------------------
    "quality_golden_cross": {
        "label": "Quality Golden Cross (ROCE + Trend)",
        "query": (
            "Return on capital employed > 20 "
            "AND Debt to equity < 0.5 "
            "AND Current price > DMA 50 "
            "AND DMA 50 > DMA 200"
        ),
    },

    # -------------------------------------------------
    # 2️⃣ High Quality Compounders
    # -------------------------------------------------
    "quality_compounders": {
        "label": "High Quality Compounders",
        "query": (
            "Return on capital employed > 25 "
            "AND Return on equity > 20 "
            "AND Debt to equity < 0.3 "
            "AND Sales growth 5Years > 10 "
            "AND Profit growth 5Years > 10"
        ),
    },

    # -------------------------------------------------
    # 3️⃣ Value + Quality (Buffett style)
    # -------------------------------------------------
    "quality_value": {
        "label": "Quality Value (Low PE + High ROCE)",
        "query": (
            "Industry PE < 15 "
            "AND Return on capital employed > 20 "
            "AND Debt to equity < 0.5 "
            "AND Current price > DMA 200"
        ),
    },

    # -------------------------------------------------
    # 4️⃣ Large & Stable Leaders
    # -------------------------------------------------
    "largecap_quality": {
        "label": "Largecap Quality Leaders",
        "query": (
            "Market Capitalization > 20000 "
            "AND Return on capital employed > 18 "
            "AND Debt to equity < 0.5 "
            "AND Current price > DMA 200"
        ),
    },

    # -------------------------------------------------
    # 5️⃣ Midcap Quality Growth
    # -------------------------------------------------
    "midcap_quality_growth": {
        "label": "Midcap Quality Growth",
        "query": (
            "Market Capitalization > 2000 "
            "AND Market Capitalization < 20000 "
            "AND Return on capital employed > 20 "
            "AND Sales growth 3Years > 12 "
            "AND Profit growth 3Years > 12 "
            "AND Debt to equity < 0.6"
        ),
    },

    # -------------------------------------------------
    # 6️⃣ Cash-Rich, Debt-Free Businesses
    # -------------------------------------------------
    "debt_free_cash_generators": {
        "label": "Debt-Free Cash Generators",
        "query": (
            "Debt to equity = 0 "
            "AND Return on capital employed > 18 "
            "AND OPM  > 15 "
            "AND Current price > DMA 200"
        ),
    },

    # -------------------------------------------------
    # 7️⃣ Consistent Earnings Machines
    # -------------------------------------------------
    "consistent_earnings": {
        "label": "Consistent Earnings (Low Volatility)",
        "query": (
            "Profit growth 5Years > 12 "
            "AND Return on capital employed > 20 "
            "AND Debt to equity < 0.5 "
            "AND Current price > DMA 200"
        ),
    },

    # -------------------------------------------------
    # 8️⃣ High ROCE + Reasonable Valuation (Sweet Spot)
    # -------------------------------------------------
    "roce_at_reasonable_price": {
        "label": "High ROCE at Reasonable Price (RARP)",
        "query": (
            "Return on capital employed > 25 "
            "AND Industry PE < 20 "
            "AND Debt to equity < 0.4 "
            "AND Current price > DMA 200"
        ),
    },

    "graham_defensive": {
    "label": "Graham Defensive (Deep Value)",
        "query": (
            "Market Capitalization > 1000 "
            "AND Current ratio > 1.5 "
            "AND Price to Earning < 15 "
            "AND Price to book value < 1.5 "
            "AND Debt to equity < 0.5 "
            "AND Earnings yield > 10"
        ),
    },

    "financial_fortress": {
    "label": "High Piotroski (Financial Strength)",
        "query": (
            "Piotroski score > 7 "
            "AND Return on capital employed > 15 "
            "AND Sales growth 3Years > 10 "
            "AND Debt to equity < 0.5 "
            "AND Average return on equity 5Years > 15"
        ),
    },

    "cheap_cash_flows": {
    "label": "Low PE + Positive Cash Flow",
        "query": (
            "Price to Earning < 12 "
            "AND Free cash flow 3years > 0 "
            "AND Cash from operations 3years > Net profit 3years "
            "AND Debt to equity < 0.3 "
            "AND Dividend yield > 1.5"
        ),
    },

    "institutional_buying": {
    "label": "Institutional Accumulation",
        "query": (
            "Change in promoter holding > 0 "
            "OR Change in institutional holding > 0.5 "
            "AND Price to Earning < Industry PE "
            "AND Return on capital employed > 18 "
            "AND Debt to equity < 0.5"
        ),
    },

    "magic_formula_india": {
    "label": "Magic Formula (Yield + ROCE)",
        "query": (
            "Earnings yield > 12 "
            "AND Return on capital employed > 22 "
            "AND Market Capitalization > 500 "
            "AND Debt to equity < 0.5 "
            "AND Interest Coverage Ratio > 4"
        ),
    },

}
