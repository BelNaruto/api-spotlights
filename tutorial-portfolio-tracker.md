---
title: Build a live stock portfolio tracker in Python
description: A short Python script that turns a list of holdings into a live portfolio value with weights, using the YH Finance Complete API on RapidAPI.
---

# Build a live stock portfolio tracker in Python

In this tutorial you will build a script that takes your holdings (ticker and number of shares), reads the live price of each stock and prints the value of every position, its weight and the portfolio total. It uses the [YH Finance Complete API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/yh-finance-complete) and about 35 lines of Python. Not investment advice.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [YH Finance Complete API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/yh-finance-complete) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Read a live price

The Stock Price endpoint (`/yhprice`) takes a `ticker` and returns `symbol`, `symbolName`, `price`, `currency` and `marketCap`. The helper retries temporary server errors.

```python
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
```

## 3. Value the portfolio

Holdings are passed as `TICKER:SHARES`. For each one we multiply the price by the shares, then sort by value and print each position's weight.

```python
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
```

## 4. Run it

```bash
python portfolio_tracker.py AAPL:10 MSFT:5 NVDA:8
```

You get one line per position and a total (illustrative numbers):

```
AAPL       10.00 x    337.46 USD =     3,374.60   55.8%  Apple
MSFT        5.00 x    400.00 USD =     2,000.00   33.1%  Microsoft
TOTAL        5,374.60
```

The complete script is in [examples/portfolio_tracker.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/portfolio_tracker.py).

## Tips

- All positions are valued in the currency the API returns (USD for US stocks). Keep holdings in one currency or convert yourself.
- Save the total every day to a CSV to chart your portfolio over time.
- The API also has summaries, financial statements, options and historical prices you can add per position.

## Next steps

- [YH Finance Complete API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/yh-finance-complete): all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
