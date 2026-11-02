---
image: /assets/vinted-deal-finder-og.jpg
title: Build a Vinted deal finder in Python
description: A short Python script that lists the cheapest Vinted listings for any search under your budget, with brand, size and favourites, using the Vinted API on RapidAPI.
---

# Build a Vinted deal finder in Python

In this tutorial you will build a script that searches Vinted for an item, keeps only listings under your budget (buyer protection fee included) and prints the cheapest ones with brand, size, favourites and a link. It uses the [Vinted API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vinted-api3) and about 45 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Vinted API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vinted-api3) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Search Vinted

The `/search` endpoint takes a `query` and optional `country`, `page`, `perPage` and `orderBy` (`relevance`, `newest_first`, `price_low_to_high` or `price_high_to_low`). It returns `items`, each with a `title`, `brand_title`, `size_title`, `favourite_count`, a `url` and `total_item_price` (the price plus the service fee). The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "vinted-api3.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def search(query, country="us", order="price_low_to_high", per_page=96):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/search", headers=HEADERS, timeout=60,
                         params={"query": query, "country": country,
                                 "orderBy": order, "perPage": per_page})
        if r.ok:
            return r.json()["items"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Keep the deals

We ask the API to sort by price, so as soon as one listing is over budget we can stop. Each deal prints on two lines: the details and the link.

```python
def main(query, max_price, country, top=10):
    shown = 0
    for item in search(query, country):
        total = float(item["total_item_price"]["amount"])
        if min(total, max_price) != total:
            break  # sorted by price, so everything after this is too expensive
        cur = item["total_item_price"]["currency_code"]
        print(f"{total:7.2f} {cur}  {item['favourite_count']:3d} favs  "
              f"{(item.get('brand_title') or '-')[:14].ljust(14)} {(item.get('size_title') or '-')[:6].ljust(6)} "
              f"{item['title'][:40]}")
        print("        " + item["url"])
        shown += 1
        if shown == top:
            break
    if shown == 0:
        print("No listings under that price.")


if __name__ == "__main__":
    a = sys.argv[1:] + ["hoodie", "20", "us"][len(sys.argv) - 1:]
    main(a[0], float(a[1]), a[2])
```

## 4. Run it

```bash
python vinted_deal_finder.py "nike hoodie" 20 us
```

You get the cheapest listings under your budget (illustrative output):

```
   5.50 USD    3 favs  Nike           M      Nike hoodie grey
        link
  12.00 USD   10 favs  Nike           M      Zip hoodie
        link
```

The complete script is in [examples/vinted_deal_finder.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/vinted_deal_finder.py).

## Tips

- Switch `order` to `newest_first` and run the script on a schedule to be the first to see new listings.
- Many favourites on a cheap listing usually means it will sell fast.
- The API also has brand search, catalog search, search filters, suggestions and a homepage feed you can add next.

## Next steps

- [Vinted API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vinted-api3) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
