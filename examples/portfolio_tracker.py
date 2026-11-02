"""Portfolio value from live prices. Uses the YH Finance Complete API on RapidAPI."""
import os, sys, time
import requests

HOST = "yh-finance-complete.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def stock_price(ticker):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/yhprice", headers=HEADERS,
                         params={"ticker": ticker}, timeout=60)
        if r.ok:
            return r.json()
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(holdings):
    rows, total = [], 0.0
    for item in holdings:
        ticker, shares = item.split(":")
        q = stock_price(ticker)
        value = q["price"] * float(shares)
        total += value
        rows.append((value, q["symbol"], q["symbolName"], q["price"], float(shares), q["currency"]))
    rows.sort(reverse=True)
    for value, symbol, name, price, shares, cur in rows:
        print(symbol.ljust(7) + f"{shares:8.2f} x {price:9.2f} {cur} = {value:12,.2f}  {value / total:5.1%}  {name}")
    print("TOTAL".ljust(7) + f"{total:12,.2f}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["AAPL:10", "MSFT:5", "NVDA:8"])
