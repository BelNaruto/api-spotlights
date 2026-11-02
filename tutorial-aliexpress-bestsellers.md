---
image: /assets/aliexpress-bestsellers-og.jpg
title: Find AliExpress bestsellers for any keyword in Python
description: A short Python script that searches AliExpress and ranks the results by units sold and rating, using the AliExpress Data API on RapidAPI.
---

# Find AliExpress bestsellers for any keyword in Python

In this tutorial you will build a script that searches AliExpress for a keyword, reads how many units each product has sold and its star rating, and prints the bestsellers first. It is a quick way to see which products in a niche actually sell. It uses the [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) and about 45 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Search products

The `/search/products` endpoint takes a `query` and optional `country`, `currency` and `page`. It returns `data.items`, each with a `title.displayTitle`, an `evaluation.starRating`, a `trade.tradeDesc` such as `184 sold` and a product `url`. The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "aliexpress-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def search(query, page=1):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/search/products", headers=HEADERS, timeout=60,
                         params={"query": query, "country": "us", "currency": "USD", "page": page})
        if r.ok:
            return r.json()["data"]["items"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Rank by units sold

`tradeDesc` is text, so a small function turns `184 sold` or `1K+ sold` into a number. We search a few pages, sort by units sold and print the top results.

```python
def units_sold(text):
    """Turn '184 sold' or '1K+ sold' into a number."""
    word = (text or "").split(" ")[0].replace("+", "").replace(",", "")
    if not word:
        return 0
    if word.endswith("K"):
        return int(float(word[:-1]) * 1000)
    return int(float(word)) if word.replace(".", "").isdigit() else 0


def main(query, pages=2, top=10):
    items = []
    for page in range(1, pages + 1):
        items += search(query, page)
    items.sort(key=lambda i: units_sold(i["trade"].get("tradeDesc")), reverse=True)
    for item in items[:top]:
        sold = units_sold(item["trade"].get("tradeDesc"))
        stars = (item.get("evaluation") or {}).get("starRating") or "-"
        print(f"{sold:6d} sold  {stars} stars  {item['title']['displayTitle'][:50]}")
        print("        " + item["url"])


if __name__ == "__main__":
    main((sys.argv[1:] + ["phone case"])[0])
```

## 4. Run it

```bash
python aliexpress_bestsellers.py "phone case"
```

You get the bestsellers first (illustrative output):

```
 10000 sold  4.9 stars  Example phone case title
        https://www.aliexpress.com/item/...
  1000 sold  4.8 stars  Another phone case
        https://www.aliexpress.com/item/...
```

The complete script is in [examples/aliexpress_bestsellers.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/aliexpress_bestsellers.py).

## Tips

- Large counts are shown as ranges like `1K+`, so treat them as a lower bound.
- Run the same keyword every week and compare the numbers to spot products that are taking off.
- The API also has product details, categories, store lookups and reference data for countries and currencies you can add next.

## Next steps

- [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
