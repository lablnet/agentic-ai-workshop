import requests

def get_crypto_price(coin: str = "bitcoin") -> str:
    """Get current price of a cryptocurrency in USD."""
    res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd").json()
    return f"${res.get(coin.lower(), {}).get('usd', 'N/A')}"
