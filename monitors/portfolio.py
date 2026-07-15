from core.enricher import enrich


def check(portfolio, settings, state):

    print("Checking portfolio...")

    assets = enrich(portfolio, settings)

    return {
        "title": "Portfolio",
        "data": assets,
        "alerts": []
    }