"""
Column normalization layer for Screener.in extractor output.

Maps positional columns (col_1, col_2, ...)
to semantic, analysis-ready field names.
"""

from typing import Dict


# Authoritative column mapping (as confirmed)
COLUMN_MAP: Dict[str, str] = {
    "col_1": "current_price",
    "col_2": "pe",
    "col_3": "market_cap",
    "col_4": "dividend_yield",
    "col_5": "net_profit_qtr",
    "col_6": "qtr_profit_var_pct",
    "col_7": "sales_qtr_rs_cr",
    "col_8": "qtr_sales_var_pct",
    "col_9": "roce_pct",
    "col_10": "dma_50",
    "col_11": "dma_200",
}


# def normalize_row(row: Dict[str, str]) -> Dict[str, str]:
#     """
#     Convert raw Screener extractor row into a normalized structure.

#     Input example:
#     {
#         "Company": "Nestle India",
#         "col_1": "1293.80",
#         "col_2": "83.33",
#         ...
#     }

#     Output example:
#     {
#         "company": "Nestle India",
#         "current_price": "1293.80",
#         "pe": "83.33",
#         ...
#     }
#     """
#     normalized: Dict[str, str] = {
#         "company": row.get("Company")
#     }

#     for raw_col, semantic_col in COLUMN_MAP.items():
#         normalized[semantic_col] = row.get(raw_col)

#     return normalized


def normalize_row(row: dict) -> dict:
    return {
        "company": row.get("company"),
        "symbol": row.get("symbol"),
        "current_price": row.get("col_1"),
        "pe": row.get("col_2"),
        "market_cap": row.get("col_3"),
        "dividend_yield": row.get("col_4"),
        "net_profit_qtr": row.get("col_5"),
        "qtr_profit_var_pct": row.get("col_6"),
        "sales_qtr_rs_cr": row.get("col_7"),
        "qtr_sales_var_pct": row.get("col_8"),
        "roce_pct": row.get("col_9"),
        "dma_50": row.get("col_10"),
        "dma_200": row.get("col_11"),
    }
