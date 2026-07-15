from providers.yahoo import get_stocks
from providers.coingecko import get_crypto
from providers.exchangerate import get_rates, convert


def enrich(portfolio, settings):

    base_currency = settings["base_currency"]

    rates_cache = {}

    assets = []

    stock_market = get_stocks(
        [stock["ticker"] for stock in portfolio["stocks"]]
    )

    crypto_market = get_crypto(
        [crypto["ticker"] for crypto in portfolio["crypto"]]
    )

    assets.extend(
        enrich_assets(
            portfolio["stocks"],
            stock_market,
            "stock",
            base_currency,
            rates_cache
        )
    )

    assets.extend(
        enrich_assets(
            portfolio["crypto"],
            crypto_market,
            "crypto",
            base_currency,
            rates_cache
        )
    )

    return assets


def enrich_assets(
    portfolio_assets,
    market_data,
    asset_type,
    base_currency,
    rates_cache
):

    assets = []

    for asset in portfolio_assets:

        market = market_data.get(asset["ticker"])

        if market is None:
            continue

        market_currency = market["market_currency"]
        display_currency = asset["display_currency"]

        display_price = convert_price(
            market["price"],
            market_currency,
            display_currency,
            rates_cache
        )

        base_price = convert_price(
            market["price"],
            market_currency,
            base_currency,
            rates_cache
        )

        assets.append({

            "type": asset_type,

            "ticker": asset["ticker"],

            "name": asset["name"],

            "quantity": asset["quantity"],

            "display_currency": display_currency,

            "market_currency": market_currency,

            "base_currency": base_currency,

            "current_price": round(display_price, 2),

            "base_price": round(base_price, 2),

            "position_value": round(
                display_price * asset["quantity"],
                2
            ),

            "base_position_value": round(
                base_price * asset["quantity"],
                2
            ),

            "daily_change": round(
                market["daily_change"],
                2
            ),

            "alerts": asset.get("alerts")

        })

    return assets


def convert_price(
    amount,
    from_currency,
    to_currency,
    rates_cache
):

    if from_currency == to_currency:
        return amount

    if from_currency not in rates_cache:
        rates_cache[from_currency] = get_rates(
            from_currency
        )

    return convert(
        amount,
        rates_cache[from_currency],
        to_currency
    )