from typing import Dict
from app.validators.golden_cross import is_golden_cross
from app.validators.death_cross import is_death_cross
from app.validators.trend_strength import calculate_trend_strength
from app.validators.volume_breakout import is_volume_breakout


def score_stock(stock: Dict[str, str]) -> int:
    score = 0

    # Golden / Death Cross
    if is_golden_cross(stock):
        score += 30
    if is_death_cross(stock):
        score -= 40

    # Trend strength
    strength = calculate_trend_strength(stock)
    if strength is not None:
        if strength > 0.10:
            score += 30
        elif strength > 0.05:
            score += 20
        elif strength > 0.02:
            score += 10

    # ROCE
    try:
        roce = float(stock.get("roce_pct", "0"))
        if roce > 25:
            score += 20
        elif roce > 15:
            score += 10
    except ValueError:
        pass

    # Volume breakout (optional)
    if is_volume_breakout(stock):
        score += 20

    return score
