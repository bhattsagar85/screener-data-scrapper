from typing import Dict, Optional


def _to_float(value: Optional[str]) -> Optional[float]:
    try:
        if value in (None, "", "-"):
            return None
        return float(value.replace(",", ""))
    except ValueError:
        return None


def calculate_trend_strength(stock: Dict[str, str]) -> Optional[float]:
    """
    Returns trend strength as a ratio.
    Example: 0.08 = strong uptrend
    """
    dma_50 = _to_float(stock.get("dma_50"))
    dma_200 = _to_float(stock.get("dma_200"))

    if dma_50 is None or dma_200 is None or dma_200 == 0:
        return None

    return (dma_50 - dma_200) / dma_200
