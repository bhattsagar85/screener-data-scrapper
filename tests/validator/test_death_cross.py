from app.validators.death_cross import is_death_cross


def test_valid_death_cross():
    stock = {
        "current_price": "90",
        "dma_50": "100",
        "dma_200": "110",
    }
    assert is_death_cross(stock) is True


def test_invalid_death_cross():
    stock = {
        "current_price": "105",
        "dma_50": "100",
        "dma_200": "110",
    }
    assert is_death_cross(stock) is False


def test_missing_data():
    stock = {
        "current_price": "",
        "dma_50": "100",
        "dma_200": "110",
    }
    assert is_death_cross(stock) is False
