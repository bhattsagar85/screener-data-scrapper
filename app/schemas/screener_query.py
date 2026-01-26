from typing import List
from pydantic import BaseModel, Field


# -----------------------------
# Atomic Query Condition
# -----------------------------

class QueryCondition(BaseModel):
    field: str = Field(
        description="Screener field name (e.g. DMA 50, ROCE, Close Price)"
    )

    operator: str = Field(
        description="Comparison operator (>, <, =)"
    )

    value: str = Field(
        description="Right-hand value of the condition"
    )

    class Config:
        extra = "forbid"


# -----------------------------
# Screener Query Schema
# -----------------------------

class ScreenerQuerySchema(BaseModel):
    query_string: str = Field(
        description="Final Screener.in query DSL string"
    )

    conditions: List[QueryCondition] = Field(
        description="Atomic breakdown of the Screener query"
    )

    explanation: str = Field(
        description="Human-readable explanation of the query"
    )

    expected_columns: List[str] = Field(
        default_factory=lambda: [
            "Name",
            "Current Price",
            "Market Capitalization",
            "P/E"
        ],
        description="Columns to extract from Screener results"
    )

    class Config:
        extra = "forbid"
