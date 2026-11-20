---
title: Check live IKEA prices for the trending searches with Python
image: /assets/ikea-trending-prices-og.jpg
description: A Python script that pulls IKEA's trending searches and categories and then checks the price range and cheapest item for each, using the IKEA Data API on RapidAPI.
---

# Check live prices for IKEA's trending searches

IKEA publishes a short list of trending searches. This script takes that list and runs a live search for each term to show how many products exist and what they cost. It uses the [IKEA Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/ikea-data-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The first endpoint is `GET /search/trending` (optional `localeCode`). It returns `data.searchSuggestions` (`text`, `type`) and `data.categories` (`id`, `name`). Each suggestion is then searched with `GET /search`. Full script: [`examples/ikea_trending_prices.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/ikea_trending_prices.py).

```python
trend = call("/search/trending")
for s in trend["searchSuggestions"]:
    data = call("/search", query=s["text"], type="normal", perPage=24)
    print(s["text"], data["pagination"]["totalAvailable"])
```

```bash
python ikea_trending_prices.py
```

## Real output (20 Nov 2026)

Trending categories: Dressers & chests of drawers, Bookshelves & bookcases, Bed frames, PAX frames for hinge doors. Trending searches, with prices in USD for the first page of results:

| Search | Results | Min | Max | Cheapest item |
|--------|---------|-----|-----|---------------|
| dresser | 483 | 69.99 | 649.99 | RAST (3-drawer dresser) |
| desk | 189 | 7.50 | 379.99 | ADILS (Leg) |
| kallax | 256 | 20.00 | 299.99 | KALLAX (Insert with 1 shelf) |
| billy bookcase | 285 | 25.00 | 287.00 | KOMPLEMENT (Shelf) |

## Things to know

- The cheapest hit is often a spare part, not the product: a table leg for `desk` and a shelf for `billy bookcase`. Filter on `typeName` before comparing prices.
- Only the first page is used here, so min and max describe that page, not all results.
- The trending endpoint returned 4 searches and 4 categories at the time of the run, with empty `pages` and `products` lists.

## Ideas

- Store the trending list daily and see which terms appear and disappear.
- Skip results whose `typeName` is not what you searched for.
