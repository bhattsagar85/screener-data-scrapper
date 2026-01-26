from app.validators.trend_strength import calculate_trend_strength


def test_trend_strength_positive():
    stock = {
        "dma_50": "110",
        "dma_200": "100",
    }
    strength = calculate_trend_strength(stock)
    assert round(strength, 2) == 0.10


def test_trend_strength_negative():
    stock = {
        "dma_50": "90",
        "dma_200": "100",
    }
    strength = calculate_trend_strength(stock)
    assert round(strength, 2) == -0.10


def test_missing_data():
    stock = {
        "dma_50": "",
        "dma_200": "100",
    }
    assert calculate_trend_strength(stock) is None
