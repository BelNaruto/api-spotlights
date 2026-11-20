---
title: Find the biggest Best Buy discounts for any search with Python
image: /assets/bestbuy-headphone-deals-og.jpg
description: A Python script that searches Best Buy, works out the percentage off for every sale item and ranks the deepest discounts with ratings, using the BestBuy USA API on RapidAPI.
---

# Find the biggest Best Buy discounts with Python

Search Best Buy for any term and get a short deal report: how many products are on sale, the average discount and the five deepest cuts with their ratings. It uses the [BestBuy USA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/bestbuy-usa).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /search` with `query` and an optional `page`. The response has `data.products`. Each product has `skuId`, `title`, `url`, `ratings` (`score`, `count`) and a `price` object with `customerPrice`, `previousPrice`, `discount` (an amount in dollars, not a percentage), `priceEventType` and `currencyName`. Full script: [`examples/bestbuy_headphone_deals.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/bestbuy_headphone_deals.py).

```python
products = call("/search", query="headphones")["products"]
for p in products:
    price = p["price"]
    print(p["title"][:40], price["customerPrice"], price["previousPrice"])
```

```bash
python bestbuy_headphone_deals.py headphones
```

## Real output (20 Nov 2026)

A search for `headphones` returned **24 products**. 20 had a price and **19 were on sale**. The average discount was **39.3%** and the dollar discount field matched `previousPrice - customerPrice` on every item. Priced items ran from 17.49 to 429 USD.

| Discount | Was | Now | Rating | Product |
|----------|-----|-----|--------|---------|
| 67% | $449.95 | $149.95 | 4.5 (30 ratings) | JBL Tour One M3 |
| 57% | $209.99 | $89.99 | 4.8 (775) | Skullcandy Crusher Evo |
| 50% | $299.99 | $149.99 | 4.7 (5,486) | Beats Studio Pro |
| 50% | $199.99 | $99.99 | 4.8 (2,438) | Beats Solo 4 |
| 50% | $239.99 | $119.99 | 4.8 (1,987) | Skullcandy Crusher ANC 2 |

## Things to know

- 4 of the 24 products came back with all price fields null: both Shokz OpenRun models, the Bose QuietComfort and the Sony WH-1000XM5. These are popular items, so the script lists the ones without a price instead of silently skipping them.
- `model`, `color` and `variations` were empty for every product in this search.
- `priceEventType` was `onSale` for 19 items and `regular` for 1.
- Ratings are the Best Buy customer ratings, with the number of reviews in `ratings.count`.

## Ideas

- Run it for several terms (`laptops`, `tvs`) and compare the average discount.
- Store the results daily to see when a product's price falls.
