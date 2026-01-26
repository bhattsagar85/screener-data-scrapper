from app.validators.golden_cross import is_golden_cross


def test_valid_golden_cross():
    stock = {
        "current_price": "120",
        "dma_50": "110",
        "dma_200": "100",
    }
    assert is_golden_cross(stock) is True


def test_invalid_golden_cross():
    stock = {
        "current_price": "105",
        "dma_50": "110",
        "dma_200": "100",
    }
    assert is_golden_cross(stock) is False


def test_missing_data():
    stock = {
        "current_price": "120",
        "dma_50": "",
        "dma_200": "100",
    }
    assert is_golden_cross(stock) is False
