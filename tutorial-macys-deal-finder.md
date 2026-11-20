---
title: Build a Macy's deal finder that ranks search results by discount (Python)
description: A Python script that searches Macy's for any product and ranks the results by discount, price and reviews, using the Macy's API on RapidAPI.
---

# Build a Macy's deal finder in Python

Search Macy's for a product and rank the results by discount, with current price, regular price and review score. It uses the [Macy's API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/macys4).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /api/search/product` with `q`, `perPage`, `pageIndex`, `currencyCode` and `regionCode`. Each product has a `priceSummary` (`current`, `regular`, `percentOff`, `promotion`) and `detail.reviewStatistics.aggregate` (`rating`, `count`). Full script: [`examples/macys_deal_finder.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/macys_deal_finder.py).

```python
result = call("/api/search/product", q="levi's 501 jeans", perPage=10)
for p in result["products"]:
    s = p["priceSummary"]
    print(s["percentOff"], s["current"], s["regular"], p["detail"]["name"])
```

```bash
python macys_deal_finder.py "levi's 501 jeans" 10
```

## Real output (20 Nov 2026)

The search returned 253 matching products (26 pages of 10). The first page:

| Product | Current | Regular | % off (API) | Rating (reviews) |
|---------|---------|---------|-------------|------------------|
| Men's 501 Original Shrink-to-Fit Non-Stretch Jeans | $47.70 | $79.50 | 30 | 4.3 (8,825) |
| Men's 501 Regular-Fit Button Fly Non-Stretch Jeans | $23.83 | $79.50 | 30 | 4.3 (7,761) |
| Men's 501 Straight-Fit Button Fly Stretch Jeans | $59.46 | $84.95 | 30 | 4.3 (8,876) |
| Women's 501 Curve High-Rise Straight-Leg Jeans | $59.99 | $84.95 | 29 | 3.8 (368) |
| Men's 501 Original Straight-Fit Lightweight Denim | $59.46 | $84.95 | 30 | 4.6 (89) |
| Premium Women's 501 90's Mid-Rise 30" Straight-Fit | $59.99 | $110.00 | 40 | 4.5 (413) |
| Men's Premium 501 Original Straight-Fit Jeans | $110.00 | $110.00 | none | 4.6 (522) |
| Men's 501 Relaxed Jeans | $59.46 | $84.95 | 30 | 4.7 (130) |
| Men's 501 Regular-Fit Button Fly Jeans | $50.97 | $84.95 | 30 | 4.3 (3,631) |
| Men's 501 Relaxed-Fit Jeans | $59.46 | $84.95 | 30 | 4.1 (8) |

Note that `current` is the lowest price across colors and sizes (the first item ranges from $47.70 to $59.46), so the dollar figure can imply a bigger discount than `percentOff`: the Button Fly Non-Stretch pair shows $23.83 against $79.50 regular, but the API reports 30. Compute your own discount from `current` and `regular` if you need the best-case saving.

## Ideas

- Page through results with `pageIndex` and store them to track price drops.
- Only alert when the discount and the review count both pass a threshold.
