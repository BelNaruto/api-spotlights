---
title: Build a Best Buy price and review tracker in Python
description: A short Python script that tracks Best Buy prices and ratings and prints every price drop, using the BestBuy USA API on RapidAPI.
image: /assets/bestbuy-usa-api-og.jpg
---

![Best Buy price tracker](assets/bestbuy-usa-api.png)

# Build a Best Buy price and review tracker in Python

In this tutorial you will build a script that searches Best Buy for a product, reads the live price and rating of the top results, and tells you whenever a price drops on the next run. It uses the [BestBuy USA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/bestbuy-usa) and about 50 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [BestBuy USA API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/bestbuy-usa) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

The helper returns the `data` part of the response and retries temporary 502/503/504 errors.

```python
HOST = "bestbuy-usa.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            return body.get("data", body)
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(int(r.headers.get("Retry-After", 5)))
            continue
        r.raise_for_status()
```

## 3. Find products

`/search` takes a `query` and returns `products` with `skuId`, `title` and `ratings` (score and count). Search results can contain the same SKU twice, so we de-duplicate. Prices are not filled in search results, so we read them in the next step.

```python
def search(query, limit=5):
    data = call("/search", query=query)
    products = {}
    for p in data["products"]:
        products.setdefault(p["skuId"], p)
    return list(products.values())[:limit]
```

## 4. Read the live price

`/product/price` takes a `sku` and returns the current `customerPrice` (a number) plus `previousPrice` and savings fields.

```python
def current_price(sku):
    return call("/product/price", sku=sku)["customerPrice"]
```

## 5. Compare with last run

Prices are saved to `bestbuy_prices.json`. On each run, anything cheaper than before is printed as a drop, together with the product rating.

```python
old = before.get(sku)
if old is not None and price != old and price == min(price, old):
    print(f"DROP  ${old:.2f} to ${price:.2f}  {p['title']}  (rating {score})")
```

## 6. Run it

```bash
python bestbuy_price_tracker.py "sony headphones"
```

The first run saves a baseline. Run it again later (or schedule it with cron) and you will see lines like:

```
DROP  $349.99 to $299.99  Sony WH-1000XM5 Wireless Noise Cancelling Headphones  (rating 4.6)
      $199.99  Sony WH-CH720N Wireless Headphones  (rating 4.4)
```

The complete script is in [examples/bestbuy_price_tracker.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/bestbuy_price_tracker.py).

## Tips

- Each tracked product costs one price request, so keep `limit` small or track a fixed list of SKUs.
- Schedule the script with cron (`0 */6 * * *`) and send yourself an email or Telegram message instead of printing.
- The API also has review and recommendation endpoints you can add to the same script.

## Next steps

- [BestBuy USA API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/bestbuy-usa): all endpoints, plans and live playground.
- [API guide](bestbuy-usa-api): features and use cases.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
