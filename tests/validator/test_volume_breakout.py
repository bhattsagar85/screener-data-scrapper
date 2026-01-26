from app.validators.volume_breakout import is_volume_breakout


def test_volume_breakout_true():
    stock = {
        "current_volume": "300000",
        "avg_volume_10d": "100000",
    }
    assert is_volume_breakout(stock) is True


def test_volume_breakout_false():
    stock = {
        "current_volume": "120000",
        "avg_volume_10d": "100000",
    }
    assert is_volume_breakout(stock) is False


def test_missing_volume_data():
    stock = {
        "current_volume": "",
        "avg_volume_10d": "100000",
    }
    assert is_volume_breakout(stock) is False
