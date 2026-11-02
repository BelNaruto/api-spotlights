---
title: Build an Etsy price and favorites tracker in Python
description: A short Python script that tracks Etsy listing prices and favorites and flags price drops, using the Etsy API on RapidAPI.
image: /assets/etsy-price-tracker-og.jpg
---

# Build an Etsy price and favorites tracker in Python

In this tutorial you will build a script that searches Etsy for a keyword, reads the live price and favorites count of the top listings, and flags price drops and new favorites on the next run. It uses the [Etsy API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/etsy-api2) and about 50 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Etsy API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/etsy-api2) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

Every response has `success` and `data`. The helper returns `data` and retries temporary server errors.

```python
import json, os, sys, time
import requests

HOST = "etsy-api2.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}
STATE = "etsy_prices.json"

def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Find listings

`/product/search` takes a `query` and returns `results`, each with a `listingId`, a `title`, an image and shop info. Search results do not include the price, so we read it in the next step.

```python
def search(query, limit=5):
    return call("/product/search", query=query)["results"][:limit]
```

## 4. Read price and favorites

`/product/description/v5` takes a `listingId` and returns the full listing: `price.amount`, `price.currency`, `favorites`, `quantity`, `isSoldOut`, tags and more. Some listings come back with empty fields, so the script skips them.

```python
def details(listing_id):
    return call("/product/description/v5", listingId=listing_id)
```

## 5. Compare with last run

Prices and favorites are saved to `etsy_prices.json`. On each run, a cheaper price is printed as a `DROP` and a higher favorites count shows how many new favorites a listing gained.

```python
def main(query):
    try:
        before = json.load(open(STATE))
    except FileNotFoundError:
        before = {}
    now = {}
    for item in search(query):
        lid = str(item["listingId"])
        d = details(lid)
        price, favs = d["price"]["amount"], d["favorites"]
        if price is None:
            print(f"      no price yet  {item['title'][:60]}")
            continue
        now[lid] = {"price": price, "favorites": favs}
        old = before.get(lid)
        tag = "      "
        if old and price != old["price"] and price == min(price, old["price"]):
            tag = "DROP  "
        extra = f"  (+{favs - old['favorites']} favorites)" if old and favs != old["favorites"] else ""
        print(f"{tag}${price:.2f}  {favs} favorites  {item['title'][:50]}{extra}")
    json.dump({**before, **now}, open(STATE, "w"))


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "handmade candle")
```

## 6. Run it

```bash
python etsy_price_tracker.py "handmade candle"
```

The first run saves a baseline. Run it again later (or schedule it with cron) and you will see lines like (illustrative numbers):

```
DROP  $7.50  14 favorites  Hand poured soy candle  (+4 favorites)
      $5.00  14 favorites  Beeswax taper candles
```

The complete script is in [examples/etsy_price_tracker.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/etsy_price_tracker.py).

## Tips

- Each tracked listing costs one details request, so keep `limit` small or track a fixed list of listing ids.
- Favorites growth is a good early signal of a trending product.
- Schedule the script with cron (`0 */6 * * *`) and send yourself an email or Telegram message.

## Next steps

- [Etsy API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/etsy-api2): all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
