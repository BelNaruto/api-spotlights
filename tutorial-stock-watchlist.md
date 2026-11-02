---
title: Build a live stock watchlist in Python
description: A short Python script that looks up tickers and prints a live watchlist with day change, using the Seeking Alpha API on RapidAPI.
image: /assets/seeking-alpha-api-og.jpg
---

![Stock watchlist](assets/seeking-alpha-api.png)

# Build a live stock watchlist in Python

In this tutorial you will build a script that takes a list of tickers and prints a watchlist sorted by day change, with the latest price and the data delay. It uses the [Seeking Alpha API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/seeking-alpha-api) and about 45 lines of Python. Unofficial data, not investment advice.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Seeking Alpha API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/seeking-alpha-api) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

The helper returns the JSON body and retries temporary server errors.

```python
import os, re, sys, time
import requests

HOST = "seeking-alpha-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Turn a ticker into a stock id

The price endpoint takes a numeric `sa_id`, so we first call `/search`. It returns `search_result.symbols`, each with an `id`, a `name` (the ticker) and a `content` (the company). We pick the exact ticker match.

```python
def find_id(ticker):
    """/search returns symbols with a numeric id (sa_id). Pick the exact ticker match."""
    symbols = call("/search", query=ticker, limit=10)["search_result"]["symbols"]
    for s in symbols:
        if s["name"].upper() == ticker.upper():
            return s["id"], re.sub(r"\x3c/?b\x3e", "", s["content"])  # strip highlight tags
    return None, None
```

## 4. Read the live quote

`/price` takes the `sa_id` and returns `real_time_quote`, a list whose first item has `last`, `prev_close`, `high`, `low`, `volume` and `info` (for example `Delayed`).

```python
def quote(sa_id):
    return call("/price", sa_id=sa_id)["real_time_quote"][0]
```

## 5. Print the watchlist

Compute the day change from `last` and `prev_close`, sort the best movers first and print one line per stock.

```python
def main(tickers):
    rows = []
    for t in tickers:
        sa_id, name = find_id(t)
        if sa_id is None:
            print(f"{t}: not found")
            continue
        q = quote(sa_id)
        last, prev = q.get("last"), q.get("prev_close")
        change = (last - prev) / prev * 100 if last and prev else 0.0
        rows.append((change, t.upper(), name, last, q.get("volume"), q.get("info")))
    rows.sort(reverse=True)
    for change, t, name, last, volume, info in rows:
        print(t.ljust(7) + f"{last:10.2f}  {change:+6.2f}%  {name[:28].ljust(28)} ({info})")


if __name__ == "__main__":
    main(sys.argv[1:] or ["AAPL", "MSFT", "NVDA", "TSLA"])
```

## 6. Run it

```bash
python stock_watchlist.py AAPL MSFT NVDA TSLA
```

You get one line per ticker, best mover first (illustrative numbers):

```
NVDA      190.12   +1.84%  NVIDIA Corporation           (Delayed)
```

The complete script is in [examples/stock_watchlist.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/stock_watchlist.py).

## Tips

- Cache the `sa_id` of each ticker in a file so each refresh costs one request per stock.
- Run it in a loop with `time.sleep(60)` for a simple live board, or schedule it with cron.
- The API also has analyst ratings, earnings estimates and news endpoints you can add per ticker.

## Next steps

- [Seeking Alpha API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/seeking-alpha-api): all endpoints, plans and live playground.
- [API guide](seeking-alpha-api): features and use cases.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
