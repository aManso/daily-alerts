import requests


URL = "https://api.coingecko.com/api/v3/simple/price"


def get_crypto(tickers):

    params = {
        "ids": ",".join(tickers),
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }

    response = requests.get(URL, params=params)

    response.raise_for_status()

    data = response.json()

    result = {}

    for ticker in tickers:

        if ticker not in data:
            continue

        result[ticker] = {

            "price": data[ticker]["usd"],

            "daily_change": data[ticker]["usd_24h_change"],

            "market_currency": "USD"

        }

    return result