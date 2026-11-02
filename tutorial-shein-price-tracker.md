---
title: Build a SHEIN price-drop tracker in Python
description: A 60-line Python script that tracks SHEIN prices and prints every price drop, using the Shein Data API on RapidAPI.
image: /assets/shein-data-api-og.jpg
---

![SHEIN price tracker](assets/shein-data-api.png)

# Build a SHEIN price-drop tracker in Python

In this tutorial you will build a small script that searches SHEIN for a keyword, remembers the price of every result, and tells you whenever a price drops on the next run. It uses the [Shein Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shein-data-api) and about 60 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Shein Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shein-data-api) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

Every response has the same envelope: `success`, `data` and `error`. The helper returns `data`, raises a readable error, and retries the temporary 502/503/504 errors using the `Retry-After` header, as the API docs recommend.

```python
def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        body = r.json()
        if body.get("success"):
            return body["data"]
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(int(r.headers.get("Retry-After", 5)))
            continue
        raise RuntimeError(f"{body['error']['code']}: {body['error']['message']}")
```

## 3. Find products

`/search/products` takes a keyword and returns cards with `goods_id`, `name` and price. We use `sort=popular` so we track what people actually buy.

```python
def search(query, limit=20):
    data = call("/search/products", query=query, country="US", limit=limit, sort="popular")
    return {p["goods_id"]: p["name"] for p in data["products"]}
```

## 4. Read live prices in batches

`/product/price/batch` returns live price and stock for up to 10 products in one call, so 20 products cost 2 requests instead of 20.

```python
def current_prices(goods_ids):
    prices = {}
    for i in range(0, len(goods_ids), 10):
        data = call("/product/price/batch", goods_ids=",".join(goods_ids[i:i + 10]))
        for item in data["results"]:
            if item["ok"]:
                prices[item["goods_id"]] = item["data"]["price"]["sale"]["amount"]
    return prices
```

## 5. Compare with last run

Prices are saved to `prices.json`. On each run, anything cheaper than before is printed as a drop.

```python
for goods_id, price in now.items():
    old = before.get(goods_id)
    if old is not None and price != old and price == min(price, old):
        print(f"DROP  ${old:.2f} to ${price:.2f}  {names[goods_id]}")
```

## 6. Run it

```bash
python shein_price_tracker.py "summer dress"
```

The first run saves a baseline. Run it again later (or schedule it with cron) and you will see lines like:

```
DROP  $14.99 to $11.49  Floral Print Sweetheart Neck Dress
Tracked 20 products for 'summer dress'.
```

The complete script is in [examples/shein_price_tracker.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/shein_price_tracker.py).

## Tips

- Prices, currencies and stock differ per country site. Product price endpoints currently work for the **US** site, so keep `country=US`.
- Don't hammer the API: keep concurrency low and use the batch endpoint.
- Schedule the script with cron (`0 */6 * * *`) and send yourself an email or Telegram message instead of printing.

## Next steps

- [Shein Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shein-data-api): all endpoints, plans and live playground.
- [API guide](shein-data-api): features and use cases.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
