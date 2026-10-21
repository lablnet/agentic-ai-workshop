"""Cryptocurrency prices from CoinGecko."""

import logging

import requests


def get_crypto_price(coin: str = "bitcoin") -> str:
    """Get the current USD price using a CoinGecko ID, such as bitcoin or ethereum."""
    logging.info("TOOL | get_crypto_price | %s", coin)
    try:
        # Call the CoinGecko API
        response = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": coin.lower(), "vs_currencies": "usd"}, timeout=15,
        )
        # Raise an error if the request is not successful
        response.raise_for_status()
        # Get the price from the response
        price = response.json().get(coin.lower(), {}).get("usd")
        # Return the price
        return f"{coin}: {price} USD" if price is not None else f"No price found for {coin}."
    except (requests.RequestException, ValueError) as error:
        return f"Crypto API unavailable: {error}"
