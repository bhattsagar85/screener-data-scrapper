from typing import Dict, Optional


def _to_float(value: Optional[str]) -> Optional[float]:
    try:
        if value in (None, "", "-"):
            return None
        return float(value.replace(",", ""))
    except ValueError:
        return None


def is_death_cross(stock: Dict[str, str]) -> bool:
    """
    Validate Death Cross condition:
    current_price < dma_50 < dma_200
    """
    price = _to_float(stock.get("current_price"))
    dma_50 = _to_float(stock.get("dma_50"))
    dma_200 = _to_float(stock.get("dma_200"))

    if price is None or dma_50 is None or dma_200 is None:
        return False

    return price < dma_50 < dma_200
