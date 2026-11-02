---
image: /assets/stock-performance-snapshot-og.jpg
title: Build a stock dividend history tracker in Python (with the country code)
description: A short Python script that prints a stock's dividend history, yield and growth, and shows how to pass the required country code, using the Investing.com Ultimate API on RapidAPI.
---

# Build a stock dividend history tracker in Python (with the country code)

In this tutorial you will build a script that prints a stock's dividend history, yield and growth, and compares the latest payment with a year earlier. You will also see why the `country` parameter matters. It uses the [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The dividends endpoint (`/v2/stocks/dividends`) takes `symbol` and `country`. **Always send `country`** (a 2-letter code such as US, DE or PT): the same ticker can exist in several countries. In our live tests the stock quote endpoint (`/v2/stocks`) returned a 400 error for AAPL without `country`, because that symbol exists in 5 countries. The list of valid codes is at `/v2/reference/countries`. The response has `data.summary` (annualized payout, yield, five year growth) and `data.history` with `ex_date`, `payment_date`, `amount` and `frequency`.

## 3. The script

Save this as `dividend_history.py`. It retries temporary server errors.

```python
import os
import sys
import time

import requests

HOST = "investing-com-ultimate-api.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}


def dividends(symbol, country="US"):
    # country is required: the same ticker can exist in several countries
    for attempt in range(3):
        r = requests.get(
            f"https://{HOST}/v2/stocks/dividends",
            headers=HEADERS,
            params={"symbol": symbol, "country": country},
            timeout=60,
        )
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()


def main(symbol, country="US"):
    body = dividends(symbol, country)
    data, meta = body["data"], body["meta"]
    summary, history = data["summary"], data["history"]
    print(f"{meta['instrument']['name']} ({symbol.upper()}, {country.upper()}) in {meta['currency']}")
    print(f"Annualized payout {summary['annualized_payout']}  yield {summary['dividend_yield']:.2f}%  5y growth {summary['five_year_growth']:.1f}%")
    print("\nEX-DATE      PAID         AMOUNT")
    for item in history[:6]:
        print(f"{item['ex_date']}   {item['payment_date']}   {item['amount']:.2f}  {item['frequency']}")
    if history[4:]:
        newest, year_ago = history[0]["amount"], history[4]["amount"]
        print(f"\nLatest payment vs a year earlier: {100 * (newest / year_ago - 1):+.1f}%")


if __name__ == "__main__":
    args = sys.argv[1:] + ["AAPL", "US"]
    main(args[0], args[1])
```

## 4. Run it

```bash
python dividend_history.py AAPL US
```

Real output for Apple (country US):

```
Apple Inc (AAPL, US) in USD
Annualized payout 1.08  yield 0.31%  5y growth 4.7%

EX-DATE      PAID         AMOUNT
2026-08-10   2026-08-13   0.27  quarterly
2026-05-11   2026-05-14   0.27  quarterly
2026-02-09   2026-02-12   0.26  quarterly
2025-11-10   2025-11-13   0.26  quarterly
2025-08-11   2025-08-14   0.26  quarterly
2025-05-12   2025-05-15   0.26  quarterly

Latest payment vs a year earlier: +3.8%
```

The complete script is in [examples/dividend_history.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/dividend_history.py).

## Tips

- Change the second argument to a code from `/v2/reference/countries` to look up a company listed in another country.
- Loop over a watchlist and sort by yield.
- `next_dividend_date` is empty when no payment is announced yet.

## Next steps

- [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
