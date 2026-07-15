import requests

def get_crypto_price(crypto_id, currency="eur"):
    url = "https://api.coingecko.com/api/v3/simple/price"

    r = requests.get(url, params={
        "ids": crypto_id,
        "vs_currencies": currency
    })

    data = r.json()

    return data[crypto_id][currency]

from providers.crypto import get_crypto_price

def get_crypto(portfolio):
    results = []

    for c in portfolio.get("crypto", []):
        price = get_crypto_price(c["id"])

        results.append({
            "name": c["name"],
            "price": price,
            "change_pct": c.get("change_pct", 0)
        })

    return results