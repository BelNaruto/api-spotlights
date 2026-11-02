---
title: Tear down a competitor Shopify store in Python
description: A short Python script that profiles any Shopify store (theme, catalogue size, price range, discounts) using the Shopify Stores Info API on RapidAPI.
---

# Tear down a competitor Shopify store in Python

In this tutorial you will build a script that takes the domain of any Shopify store and prints a quick teardown: theme, currency, catalogue size, shipping reach, median price, price range, how much of the catalogue is on sale and the top product types. It uses the [Shopify Stores Info API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shopify-stores-info) and about 50 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Shopify Stores Info API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shopify-stores-info) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Call the API

Two endpoints do the work. `/store/info` returns the store profile, and `/product/all` returns a page of its products with pricing already parsed (`priceMin`, `onSale`, `discountPercent`). Both take the store domain as `url`. The helper retries temporary server errors.

```python
import os, sys, time
from collections import Counter
from statistics import median
import requests

HOST = "shopify-stores-info.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def get(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Build the teardown

We read the store profile, then pull product pages until we have enough (or there is no next page), and compute the numbers.

```python
def teardown(domain, pages=2):
    info = get("/store/info", url=domain)
    products = []
    for page in range(1, pages + 1):
        data = get("/product/all", url=domain, page=page)
        products += data["products"]
        if not data["pagination"]["hasNextPage"]:
            break

    prices = [p["pricing"]["priceMin"] for p in products if p["pricing"]["priceMin"]]
    on_sale = [p for p in products if p["pricing"]["onSale"]]
    types = Counter(p["productType"] or "(none)" for p in products)

    print(f"{info['title']} ({domain})")
    print(f"  theme: {info['storeTheme']['name']}   currency: {info['storeCurrency']}")
    print(f"  catalogue: {info['availableProducts']} products, {info['publishedCollectionsCount']} collections")
    print(f"  ships to {len(info['shipstoCountries'])} countries")
    print(f"  sampled {len(products)} products: median price {median(prices):.2f}, "
          f"range {min(prices):.2f} to {max(prices):.2f}")
    print(f"  on sale: {len(on_sale)} of {len(products)} ({len(on_sale) / len(products):.0%})")
    print("  top types: " + ", ".join(f"{t} ({n})" for t, n in types.most_common(3)))


if __name__ == "__main__":
    for d in sys.argv[1:] or ["allbirds.com"]:
        teardown(d)
```

## 4. Run it

```bash
python store_teardown.py allbirds.com
```

You get a short profile per store (illustrative numbers):

```
Allbirds (allbirds.com)
  theme: Dawn   currency: USD
  catalogue: 120 products, 30 collections
  ships to 2 countries
  sampled 40 products: median price 110.00, range 18.00 to 180.00
  on sale: 12 of 40 (30%)
  top types: Shoes (28), Apparel (8), Accessories (4)
```

Pass several domains to compare competitors side by side. The complete script is in [examples/store_teardown.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/store_teardown.py).

## Tips

- Raise `pages` to sample more of the catalogue; `/product/all` also accepts `query`, `perPage` and `sortBy`.
- Run it weekly and save the results to see when a competitor starts discounting.
- The API also has store apps, contacts, social profiles, collections, blogs and a domain check, so you can enrich each store further.

## Next steps

- [Shopify Stores Info API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shopify-stores-info): all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
