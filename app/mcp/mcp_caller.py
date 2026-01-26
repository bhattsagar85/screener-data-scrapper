import requests

BASE_URL = "http://127.0.0.1:8000"

# Discover strategies
strategies = requests.get(f"{BASE_URL}/strategies").json()

# Fetch portfolio
portfolio = requests.get(
    f"{BASE_URL}/portfolio/latest",
    params={"strategy_number": 5}
).json()

print(portfolio)
