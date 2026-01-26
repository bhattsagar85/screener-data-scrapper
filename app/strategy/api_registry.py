STRATEGIES = {
    1: {
        "key": "quality_golden_cross",
        "label": "Quality Golden Cross (ROCE + Trend)",
        "query": "Return on capital employed > 20 AND Current price > DMA 50 AND DMA 50 > DMA 200",
    },
    2: {
        "key": "high_quality_compounders",
        "label": "High Quality Compounders",
        "query": "Return on capital employed > 25 AND Market Capitalization > 5000",
    },
    3: {
        "key": "quality_value",
        "label": "Quality Value (Low PE + High ROCE)",
        "query": "Industry PE < 15 AND Return on capital employed > 20",
    },
    4: {
        "key": "largecap_quality",
        "label": "Largecap Quality Leaders",
        "query": "Market Capitalization > 20000 AND Return on capital employed > 20",
    },
    5: {
        "key": "midcap_quality_growth",
        "label": "Midcap Quality Growth",
        "query": (
            "Market Capitalization > 1000 "
            "AND Market Capitalization < 20000 "
            "AND Return on capital employed > 18 "
            "AND Current price > DMA 50"
        ),
    },
    6: {
        "key": "debt_free_cash_generators",
        "label": "Debt-Free Cash Generators",
        "query": "Debt to equity = 0 AND Return on capital employed > 15",
    },
    7: {
        "key": "consistent_earnings",
        "label": "Consistent Earnings (Low Volatility)",
        "query": "Sales growth 5Years > 10 AND Profit growth 5Years > 10",
    },
    8: {
        "key": "rarp",
        "label": "High ROCE at Reasonable Price (RARP)",
        "query": "Return on capital employed > 20 AND Industry PE < 25",
    },
    9: {
        "key": "graham_defensive",
        "label": "Graham Defensive (Deep Value)",
        "query": "Price to Earning < 15 AND Price to book value < 1.5 AND Debt to equity < 0.5 AND Current ratio > 1.5",
    },
    10: {
        "key": "piotroski_strength",
        "label": "Financial Fortress (Piotroski 7+)",
        "query": "Piotroski score > 7 AND Return on capital employed > 15 AND Debt to equity < 0.5",
    },
    11: {
        "key": "cheap_cash_flows",
        "label": "Cheap Cash Flows (FCF focus)",
        "query": "Price to Earning < 12 AND Free cash flow 3years > 0 AND Operating cash flow 3years  > Return on assets 3years ",
    },
    12: {
        "key": "magic_formula",
        "label": "Magic Formula (Yield + ROCE)",
        "query": "Earnings yield > 12 AND Return on capital employed > 22 AND Debt to equity < 0.5",
    },
}