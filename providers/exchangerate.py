import requests


def get_rates(base_currency):

    url = f"https://open.er-api.com/v6/latest/{base_currency}"

    response = requests.get(url)

    response.raise_for_status()

    return response.json()["rates"]


def convert(amount, rates, to_currency):

    if to_currency not in rates:
        raise ValueError(
            f"Moneda no soportada: {to_currency}"
        )

    return amount * rates[to_currency]