from typing import Dict, Optional


def _to_float(value: Optional[str]) -> Optional[float]:
    try:
        if value in (None, "", "-"):
            return None
        return float(value.replace(",", ""))
    except ValueError:
        return None


def is_volume_breakout(
    stock: Dict[str, str],
    multiplier: float = 1.5
) -> bool:
    """
    Validate volume breakout condition.
    Requires volume data (optional).
    """
    volume = _to_float(stock.get("current_volume"))
    avg_volume = _to_float(stock.get("avg_volume_10d"))

    if volume is None or avg_volume is None:
        return False

    return volume > avg_volume * multiplier
