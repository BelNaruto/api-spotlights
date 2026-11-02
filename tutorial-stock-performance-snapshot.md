---
title: Build a stock performance snapshot in Python
description: A short Python script that prints price, 1-day, 1-month, year-to-date and 1-year performance and distance from the 52-week high for a list of stocks, using the Investing.com Ultimate API on RapidAPI.
---

# Build a stock performance snapshot in Python

In this tutorial you will build a script that takes a list of tickers and prints a one-line snapshot for each: the last price, the 1-day, 1-month, year-to-date and 1-year performance and how far the price is from its 52-week high. It uses the [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api) and about 35 lines of Python. Not investment advice.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Get a stock quote

The `/v2/stocks` endpoint takes a `symbol` (and optionally `country`, `currency` and `language`) and returns a `data` object with the name, `price` (`last`, `change`, `high`, `low`), `performance` (`1d`, `1w`, `1m`, `3m`, `6m`, `ytd`, `1y`, `3y`, `5y`), `range_52_weeks` and `fundamentals`. The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "investing-com-ultimate-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def stock(symbol):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/v2/stocks", headers=HEADERS,
                         params={"symbol": symbol}, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Print the snapshot

For each ticker we read the last price and the performance numbers, and compute how far the price is from the 52-week high.

```python
def main(symbols):
    print("SYMBOL".ljust(8) + "PRICE".rjust(9) + "1D".rjust(8) + "1M".rjust(8) +
          "YTD".rjust(8) + "1Y".rjust(8) + "  FROM 52W HIGH")
    for symbol in symbols:
        d = stock(symbol)
        p, perf, rng = d["price"], d["performance"], d["range_52_weeks"]
        off_high = (p["last"] / rng["high"] - 1) * 100
        print(symbol.upper().ljust(8) + f"{p['last']:9.2f}" + f"{perf['1d']:+7.1f}%" +
              f"{perf['1m']:+7.1f}%" + f"{perf['ytd']:+7.1f}%" + f"{perf['1y']:+7.1f}%" +
              f"  {off_high:+.1f}%  {d['name']}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["AAPL", "MSFT", "NVDA"])
```

## 4. Run it

```bash
python stock_snapshot.py AAPL MSFT NVDA
```

You get one line per stock (illustrative numbers):

```
SYMBOL      PRICE      1D      1M     YTD      1Y  FROM 52W HIGH
AAPL       337.16   -2.2%   +1.1%  +23.8%  +24.7%  -4.1%  Apple Inc
```

The complete script is in [examples/stock_snapshot.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/stock_snapshot.py).

## Tips

- Add `country` to the request when a ticker exists on several exchanges.
- Use the `currency` parameter to see every price in your own currency.
- The API also has historical prices, financial statements, ratios, forecasts, dividends, news, technical summaries, ETFs, funds, currencies, crypto and an economic calendar you can add next.

## Next steps

- [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
