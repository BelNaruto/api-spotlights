---
title: Scan Fashion Nova sale prices and verify the discounts with Python
image: /assets/fashionnova-sale-scanner-og.jpg
description: A Python script that searches Fashion Nova, finds the products on sale, ranks them by discount and checks that each percentage matches the prices, using the Fashion Nova API on RapidAPI.
---

# Scan Fashion Nova sale prices with Python

Search Fashion Nova for any keyword, see how many results are on sale and how deep the discounts go, and check that the advertised percentage matches the prices. It uses the [Fashion Nova API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/fashion-nova-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /search` with `query`, `page`, `perPage` (max 40), `sortBy` (`RELEVANCE` or `PRICE`), `country` and `language`. The response has `data.products` and `data.pagination` (`totalAvailable`, `hasNextPage`). Each product has `title`, `handle`, `productType`, `variantsCount` and a `price` with `amount`, `compareAt`, `onSale`, `discountPercentage` and `currency`. Full script: [`examples/fashionnova_sale_scanner.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/fashionnova_sale_scanner.py).

```python
data = call("/search", query="dress", perPage=20, sortBy="RELEVANCE", country="US")
for p in data["products"]:
    pr = p["price"]
    print(p["title"], pr["amount"], pr["compareAt"], pr["discountPercentage"])
```

```bash
python fashionnova_sale_scanner.py dress
```

## Real output (20 Nov 2026)

`dress` reported **1,000 results**. The first page of 20 products had **all 20 on sale**, priced from 10.00 to 69.99 USD (median 22.49), with an **average discount of 44.0%**. 19 were dresses and 1 was in the `Luxe` type; all 20 were available for sale.

| Product | Now | Was | Off |
|---------|-----|-----|-----|
| Kallan Knit Dress - Black | 10.00 | 34.99 | 71% |
| Kallan Knit Dress - Blue | 10.00 | 34.99 | 71% |
| Kallan Knit Dress - White | 10.00 | 34.99 | 71% |
| Kallan Knit Dress - Pink | 10.00 | 34.99 | 71% |
| A Little Bossy Midi Dress - Black | 12.00 | 29.99 | 60% |
| Kora Midi Dress - Black | 12.00 | 24.99 | 52% |

All 20 discount percentages matched their prices (0 mismatches).

## Things to know

- Each colour is its own product (the Kallan dress appears four times), so group by the name without the colour if you want one row per style.
- `totalAvailable` is 1,000 for this query, which looks like a cap rather than an exact count.
- The data showed a store-wide sale on the day, so expect lower discount rates outside sale periods.

## Ideas

- Run it every day for `jeans` and chart the average discount.
- Alert when `compareAt` changes, which shows a price reset.
