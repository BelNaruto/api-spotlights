---
title: Check size-by-size stock and reviews for any SHEIN product with Python
image: /assets/shein-stock-and-reviews-og.jpg
description: A Python script that shows price, discount, stock per size and a review summary for one SHEIN product, using the Shein Data API on RapidAPI.
---

# Check stock per size and reviews for a SHEIN product with Python

Give the script a SHEIN `goods_id` and it prints the current price and discount, how many items are left in each size, and the review summary. It uses the [Shein Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shein-data-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

Two calls: `GET /product/price` and `GET /product/reviews`, both with `goods_id` (or a product `url`) and `country`. The price response has `price`, `stock`, `is_on_sale` and a `skus` list with `attributes`, `stock` and `in_stock` per size. The reviews response has `summary` (`average`, `total`, `total_display`) and a `reviews` list. Get `goods_id` values from the search endpoint. Full script: [`examples/shein_stock_and_reviews.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/shein_stock_and_reviews.py).

```python
price = call("/product/price", goods_id="59357445", country="US")
reviews = call("/product/reviews", goods_id="59357445", country="US")
for s in price["skus"]:
    print(s["attributes"][0]["value"], s["stock"])
```

```bash
python shein_stock_and_reviews.py 59357445 US
```

## Real output (20 Nov 2026)

Product `59357445` was **47.11 USD, now 31.84 USD (32% off)**, in stock in 5 sizes:

| Size | Stock |
|------|-------|
| S | 10 |
| M | 20 |
| L | 20 |
| XL | 20 |
| XXL | 20 |

The reviews summary showed an average of **4.79** from **270 reviews** (`total_display` says "100+"). The endpoint returned 4 reviews, all 5 stars, with dates from July 2025 to February 2026, each with the colour and size bought.

## Things to know

- The top-level `stock` field was 20, but the SKU stocks add up to 90. Use the per-size numbers.
- `sold_last_90_days` was null and `is_realtime_data` was `false`, so treat the numbers as a recent snapshot.
- The reviews summary had no `distribution_percent` (all null) and review `id` and `likes` were null.
- SHEIN only exposes its most relevant reviews, so you get a handful per call, not the full list.

## Ideas

- Alert when a size drops below 5 items.
- Pair it with the sale scanner: scan a search, then check the stock of the top 3 discounted products.
