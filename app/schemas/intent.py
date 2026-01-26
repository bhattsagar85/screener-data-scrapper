from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


# -----------------------------
# Enums (closed vocabulary)
# -----------------------------

class TrendType(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"


class TechnicalPattern(str, Enum):
    GOLDEN_CROSS = "golden_cross"
    DEATH_CROSS = "death_cross"
    PRICE_BREAKOUT = "price_breakout"
    VOLUME_SPIKE = "volume_spike"


# -----------------------------
# Technical Filters
# -----------------------------

class TechnicalFilters(BaseModel):
    patterns: List[TechnicalPattern] = Field(
        default_factory=list,
        description="Technical patterns requested by the user"
    )

    trend: Optional[TrendType] = Field(
        default=None,
        description="Overall market trend preference"
    )

    min_volume_multiplier: Optional[float] = Field(
        default=None,
        description="Volume spike threshold (e.g. 1.5x avg volume)"
    )


# -----------------------------
# Fundamental Filters
# -----------------------------

class FundamentalFilters(BaseModel):
    min_roce: Optional[float] = Field(
        default=None,
        description="Minimum Return on Capital Employed (ROCE %)"
    )

    max_pe: Optional[float] = Field(
        default=None,
        description="Maximum Price to Earnings ratio"
    )

    max_debt_to_equity: Optional[float] = Field(
        default=None,
        description="Maximum Debt to Equity ratio"
    )

    market_cap_min: Optional[float] = Field(
        default=None,
        description="Minimum market capitalization (in crores)"
    )

    market_cap_max: Optional[float] = Field(
        default=None,
        description="Maximum market capitalization (in crores)"
    )


# -----------------------------
# Intent Schema (Top Level)
# -----------------------------

class IntentSchema(BaseModel):
    raw_query: str = Field(
        description="Original user input"
    )

    technical: Optional[TechnicalFilters] = Field(
        default=None,
        description="Technical analysis related intent"
    )

    fundamentals: Optional[FundamentalFilters] = Field(
        default=None,
        description="Fundamental analysis related intent"
    )

    require_recent_data: bool = Field(
        default=True,
        description="Whether the user expects current market conditions"
    )

    class Config:
        extra = "forbid"
