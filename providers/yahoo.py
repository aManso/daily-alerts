import math
import yfinance as yf


def get_stocks(tickers):

    result = {}

    for ticker in tickers:

        try:

            stock = yf.Ticker(ticker)

            history = stock.history(period="2d")

            if history.empty or len(history) < 2:
                continue

            last = float(history["Close"].iloc[-1])
            previous = float(history["Close"].iloc[-2])

            if math.isnan(last) or math.isnan(previous):
                continue

            result[ticker] = {
                "price": last,
                "daily_change": ((last - previous) / previous) * 100,
                "market_currency": stock.fast_info.get("currency", "USD")
            }

        except Exception as e:

            print(f"Error obteniendo {ticker}: {e}")

    return result