STRATEGIES = {
1: {
    "key": "quality_momentum_alpha",
    "label": "Institutional Golden Cross (Quality + Trend)",
    "query": "Return on capital employed > 22 AND Current price > DMA 50 AND DMA 50 > DMA 200 AND Promoter holding > 45",
},
2: {
    "key": "high_quality_compounders",
    "label": "High Quality Compounders (2026 Edition)",
    "query": "Return on capital employed > 25 AND Market Capitalization > 5000 AND Sales growth 5Years > 15 AND Debt to equity < 0.2",
},
3: {
    "key": "the_gold_standard_pm",
    "label": "Portfolio Manager's Gold Standard (Alpha Generator)",
    "query": (
        "Return on capital employed > 22 AND Debt to equity < 0.3 AND Sales growth 5Years > 18 AND Profit growth 5Years > 18 AND Piotroski score > 7 AND Promoter holding > 40"
    ),
},
4: {
    "key": "largecap_bluechip_efficiency",
    "label": "Largecap Quality Leaders",
    "query": "Market Capitalization > 50000 AND Return on capital employed > 20 AND Dividend yield > 1",
},
5: {
    "key": "midcap_multibagger_hunt",
    "label": "Midcap Growth Sieve",
    "query": (
        "Market Capitalization > 2000 AND Market Capitalization < 25000 AND Return on capital employed > 20 AND Sales growth 3Years > 20 AND Current price > DMA 50"
    ),
},
6: {
    "key": "debt_free_cash_machines",
    "label": "Cash Flow Kings (Debt-Free)",
    "query": "Debt to equity = 0 AND Return on capital employed > 20 AND Operating cash flow 3years > 0",
},
7: {
    "key": "resilient_growth_cagr",
    "label": "High-Conviction Consistency",
    "query": "Sales growth 5Years > 15 AND Profit growth 5Years > 15 AND Return over 5years > 20",
},
8: {
    "key": "qgarp_valuation",
    "label": "Quality Growth at Reasonable Price (QGARP)",
    "query": "Return on capital employed > 20 AND Sales growth 5Years > 15 AND PEG Ratio < 1.2 AND Price to Earning < 35",
},
9: {
    "key": "modern_graham_value",
    "label": "Value Discovery (High Quality Deep Value)",
    "query": "Price to Earning < 18 AND Price to book value < 2.5 AND Debt to equity < 0.5 AND Return on capital employed > 15",
},
10: {
    "key": "financial_fortress",
    "label": "Piotroski 8+ Fortress",
    "query": "Piotroski score > 7 AND Return on capital employed > 18 AND Debt to equity < 0.4 AND Net profit > 10",
},
11: {
    "key": "fcf_yield_efficiency",
    "label": "Free Cash Flow Compounders",
    "query": "Price to Free Cash Flow < 25 AND Free cash flow 5years > 0 AND Return on capital employed > 20",
},
12: {
    "key": "greenblatt_magic_plus",
    "label": "Enhanced Magic Formula",
    "query": "Earnings yield > 12 AND Return on capital employed > 22 AND Debt to equity < 0.3 AND Sales growth 3Years > 12",
},
}