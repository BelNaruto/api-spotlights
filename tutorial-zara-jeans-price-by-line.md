---
image: /assets/shein-data-api-og.jpg
title: Compare Zara jeans prices by collection line in Python
description: A short Python script that searches Zara for jeans and compares prices across the TRF, Z1975 and ZW collection lines, using the Zara Data API on RapidAPI.
---

# Compare Zara jeans prices by collection line in Python

In this tutorial you will build a script that searches Zara for jeans and compares the price of each collection line (TRF, Z1975 and ZW Collection): items, cheapest, average and most expensive. It uses the [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The search endpoint (`/search`) takes `query`, `section`, `perPage` and `language`. **Send `section`**: it defaults to `HOME`, so a search for jeans without it returns no products (use `WOMAN`, `MAN` or `KID`). The response has `data.pagination.totalResults` and `data.products`; each product has `content.name` and `content.colors`, where each colour has a `price` as text. The response has no currency field, and a few products come back without a price, so the script skips those and says so.

## 3. The script

Save this as `zara_jeans_by_line.py`. It retries temporary server errors.

```python
import os
import sys
import time

import requests

HOST = "zara-data-api.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}
LINES = ("TRF", "Z1975", "ZW")


def search(query, section="WOMAN"):
    # section defaults to HOME, so always send it for fashion searches
    for attempt in range(3):
        r = requests.get(
            f"https://{HOST}/search",
            headers=HEADERS,
            params={"query": query, "section": section, "perPage": 36, "language": "en_US"},
            timeout=60,
        )
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()["data"]


def main(query):
    data = search(query)
    prices = {}
    skipped = 0
    for product in data["products"]:
        content = product["content"]
        first = content["name"].split(" ")[0].upper()
        line = first if first in LINES else "OTHER"
        price = (content["colors"][0] if content["colors"] else {}).get("price")
        if price is None:
            skipped += 1
            continue
        prices.setdefault(line, []).append(float(price))
    print(f"{data['pagination']['totalResults']} results for '{query}', first {len(data['products'])} analysed")
    print("\nLINE".ljust(10) + "ITEMS".rjust(6) + "MIN".rjust(9) + "AVG".rjust(9) + "MAX".rjust(9))
    for line, values in sorted(prices.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
        print(line.ljust(9) + str(len(values)).rjust(6) + f"{min(values):9.2f}" + f"{sum(values) / len(values):9.2f}" + f"{max(values):9.2f}")
    if skipped:
        print(f"\n{skipped} product(s) skipped because the API returned no price")


if __name__ == "__main__":
    main((sys.argv[1:] + ["jeans"])[0])
```

## 4. Run it

```bash
python zara_jeans_by_line.py jeans
```

Real output for the first 36 of 615 live results:

```
615 results for 'jeans', first 36 analysed

LINE      ITEMS      MIN      AVG      MAX
Z1975        12    49.90    59.82   119.00
TRF          15    49.90    61.90    69.90
ZW            6    59.90    79.90    89.90
OTHER         2   119.00   124.00   129.00

1 product(s) skipped because the API returned no price
```

The complete script is in [examples/zara_jeans_by_line.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/zara_jeans_by_line.py).

## Tips

- Try `dresses`, `blazer` or `sneakers`, and pass `MAN` or `KID` as the section.
- Add `sortBy=price_asc` to the request to get the cheapest items first.
- Run it weekly and save the averages to track price changes.

## Next steps

- [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
