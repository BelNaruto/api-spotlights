---
title: Find the biggest IKEA discounts for any product with Python
image: /assets/ikea-deal-finder-og.jpg
description: A Python script that searches IKEA by keyword and ranks the discounted products by percentage off, with offer dates, using the IKEA Data API on RapidAPI.
---

# Find the biggest IKEA discounts with Python

Search IKEA for any product type and get the discounted items ranked by percentage off, with the date the offer ends. It uses the [IKEA Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/ikea-data-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /search` with `query`, `type` (`normal` or `new_product`), `page`, `perPage` and `localeCode`. `data.items` is an object, not a list: the products are in `data.items.products`, next to `planner`, `content` and `categories`. Each product has `name`, `typeName`, `ratingValue`, `ratingCount`, `categoryPath` and a `salesPrice` with `numeral` (current price), `previous` (the old price), `discountPercentage`, `validFrom`, `validTo` and `tagText`. Full script: [`examples/ikea_deal_finder.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/ikea_deal_finder.py).

```python
data = call("/search", query="table", type="normal", perPage=24)
for p in data["items"]["products"]:
    s = p["salesPrice"]
    print(p["name"], s["numeral"], s.get("discountPercentage"), s["validTo"])
```

```bash
python ikea_deal_finder.py table
```

## Real output (20 Nov 2026)

`table` matched **599 results**. The first page had **22 products, 19 of them discounted** at between 19% and 23% (average 20.9%), all with the "IKEA Family price" label and valid until 24 Nov 2026. Prices are in USD.

| Product | Type | Now | Was | Off |
|---------|------|-----|-----|-----|
| VIHALS | Table | 99.99 | 129.99 | 23% |
| SKOGSTA | Dining table | 499.99 | 649.99 | 23% |
| ÅLHULT | Table | 129.99 | 169.99 | 23% |
| VIHALS | Table | 53.99 | 69.99 | 22% |
| MÖRBYLÅNGA | Table | 699.00 | 899.99 | 22% |
| IKEA PS 2026 | Table | 85.00 | 109.99 | 22% |
| TONSTAD | Extendable table | 219.99 | 279.99 | 21% |
| SANDSBERG | Table | 55.99 | 69.99 | 20% |

The best-reviewed item with 100+ ratings was the SANDSBERG table at 4.7 stars from 1,198 reviews.

## Things to know

- The prices in this snapshot belong to a time-limited Family offer, so rerun after 24 Nov to see regular prices.
- A page of 24 can include non-product entries: here 22 were products and 2 were `planner` items.

## Ideas

- Run it daily for `sofa` and alert when `validTo` changes.
- Sort by `ratingValue` to find well-reviewed bargains.
