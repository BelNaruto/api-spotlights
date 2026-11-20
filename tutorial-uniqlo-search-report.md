---
title: Build a Uniqlo search report with prices and reviews in Python
image: /assets/uniqlo-search-report-og.jpg
description: A Python script that searches Uniqlo by keyword and summarises price range, audience and the most reviewed products, handling missing promo prices, using the Uniqlo Eccommerce API on RapidAPI.
---

# Build a Uniqlo search report with Python

Search Uniqlo for any keyword and get a short report: how many products match, the price spread, who the products are for and which ones have the most reviews. It uses the [Uniqlo Eccommerce API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/uniqlo-eccommerce).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /search` with `query`, `countryIso` (both required), `page`, `perPage` and `sortBy`. `data` has `products`, `pagination` (`totalAvailable`, `hasNextPage`), `relatedKeywords`, `relaxedQueries` and `aggregations` (colours, sizes, prices, ratings, category tree). Each product has `name`, `genderName`, `prices` (`base` and `promo`), `rating` (`average`, `count`), `colors`, `sizes` and `url`. Full script: [`examples/uniqlo_search_report.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/uniqlo_search_report.py).

```python
data = call("/search", query="jacket", countryIso="US", perPage=24, sortBy="featured")
for p in data["products"]:
    pr = p["prices"]
    print(p["name"], (pr["promo"] or pr["base"])["value"], p["rating"]["count"])
```

```bash
python uniqlo_search_report.py jacket US
```

## Real output (20 Nov 2026)

`jacket` in the US matched **95 products**; the first page returned 24. Prices ran from 14.90 to 149.90 USD (median 44.90). The audience split was women 12, unisex 5, kids 4, baby 2, men 1.

| Most reviewed | For | Price | Stars | Reviews |
|---------------|-----|-------|-------|---------|
| Fluffy Yarn Fleece Full-Zip Jacket | WOMEN | 29.90 | 4.8 | 815 |
| Fleece Full-Zip Jacket | UNISEX | 39.90 | 4.6 | 316 |
| Fleece Full-Zip Jacket (Color Block) | UNISEX | 39.90 | 4.8 | 215 |
| PUFFTECH Parka | WOMEN | 69.90 | 4.5 | 194 |
| PUFFTECH Compact Vest | WOMEN | 49.90 | 4.6 | 147 |

Related searches returned: women's jackets, ultra light down jacket women, puffer jacket, Puffer jacket, rain jacket, jackets.

## Things to know

- `prices.promo` is `null` on 5 of the 24 products. On the other 19 it equals `base`, so no product on this page was discounted. Use `promo or base` as the price, and do not treat a present `promo` as a sale.
- Related keywords can repeat with different capitals (`puffer jacket` and `Puffer jacket`), so lower-case them before counting.
- The call is slow compared to most APIs, so cache the result by query and country.

## Ideas

- Run it for `down jacket` weekly and watch the median price.
- Use `aggregations.prices` to build a price histogram without fetching every page.
