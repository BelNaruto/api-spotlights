---
title: Summarise an ASOS search with prices, brands and fast sellers in Python
image: /assets/asos-search-snapshot-og.jpg
description: A Python script that searches ASOS and reports the price range, the most common brands and how many items are selling fast, using the Asos API on RapidAPI.
---

# Summarise an ASOS search with Python

Search ASOS for any keyword and get a one-screen snapshot: how many products match, the price range, the most common brands and the items flagged as selling fast. It uses the [Asos API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/asos-api6).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/search` with `query` and optional `page`, `perPage`, `currency` and `countryISO`. The response has `data.itemCount` and `data.products`. Each product has `id`, `name`, `brandName`, `colour`, `url`, `isSellingFast`, `isRestockingSoon`, `isPromotion` and a `price` object with `current`, `previous`, `rrp`, `isMarkedDown` and `currency`. Full script: [`examples/asos_search_snapshot.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/asos_search_snapshot.py).

```python
data = call("/product/search", query="jacket")
for p in data["products"]:
    print(p["brandName"], p["price"]["current"]["text"], p["name"][:40])
```

```bash
python asos_search_snapshot.py jacket
```

## Real output (20 Nov 2026)

A search for `jacket` reported **6,227 results** and returned **24 products**, all with different ids. Prices ran from **45 to 169 USD**, with a median of about 109. None of the 24 were marked down, and **19 were flagged as selling fast**. The products came from 11 brands:

| Brand | Products |
|-------|----------|
| ASOS DESIGN | 7 |
| Topshop | 3 |
| JJXX | 3 |
| Jack & Jones | 3 |
| GINA TRICOT | 2 |

The two product types returned were `Product` and `MixMatchProduct`.

## Things to know

- This call is slow. The playground request took about 23 seconds and returned 36 KB, so set a generous timeout (the script uses 90 seconds) and cache results.
- The suggestions endpoint counts 4,776 results for the same word, against 6,227 here. Treat both counts as estimates.
- `previous`, `rrp` and `lowestPriceInLast30Days` were empty for every product in this search, so check `isMarkedDown` before you compute a discount.
- The first page only. Use `page` to go further.

## Ideas

- Run it for several keywords and compare the median price per brand.
- Track how many of the first 24 results are selling fast each day.
