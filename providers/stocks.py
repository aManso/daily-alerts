import yfinance as yf

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.history(period="2d")

    if info.empty:
        return None

    last_close = info["Close"].iloc[-1]
    prev_close = info["Close"].iloc[-2]

    change_pct = ((last_close - prev_close) / prev_close) * 100

    return {
        "price": round(last_close, 2),
        "change_pct": round(change_pct, 2)
    }

from providers.stocks import get_stock_data

def get_stocks(portfolio):
    results = []

    for stock in portfolio["stocks"]:
        data = get_stock_data(stock["ticker"])

        if data:
            results.append({
                "name": stock["name"],
                "price": data["price"],
                "change_pct": data["change_pct"]
            })

    return results