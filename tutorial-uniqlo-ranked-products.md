---
title: Analyse Uniqlo's ranked products with ratings and reviews in Python
image: /assets/uniqlo-ranked-products-og.jpg
description: A Python script that fetches Uniqlo's ranked product list and summarises prices, ratings, review counts and colour choice, using the Uniqlo Eccommerce API on RapidAPI.
---

# Analyse Uniqlo's ranked products with Python

One call returns Uniqlo's ranked product list for a country. The script turns it into a compact table with price, rating, review count and number of colours. It uses the [Uniqlo Eccommerce API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/uniqlo-eccommerce).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/ranked` with `countryIso` (optional) and `limit` (required). The response is `data.products`, with the same product fields as search: `name`, `genderName`, `prices`, `rating`, `colors`, `sizes`, `l1Id` and `url`. Full script: [`examples/uniqlo_ranked_products.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/uniqlo_ranked_products.py).

```python
products = call("/product/ranked", countryIso="US", limit=24)["products"]
for i, p in enumerate(products[:10], 1):
    print(i, p["name"], p["rating"]["average"], p["rating"]["count"])
```

```bash
python uniqlo_ranked_products.py US 24
```

## Real output (20 Nov 2026)

**24 ranked products** in the US: prices from 14.90 to 149.90 USD (median 44.90). The average rating was **4.67** from **18,619 reviews** in total. Audience: women 15, unisex 6, men 3.

| # | Product | For | Price | Stars | Reviews | Colours |
|---|---------|-----|-------|-------|---------|---------|
| 1 | Wide Sweatpants | UNISEX | 49.90 | 4.8 | 2,691 | 9 |
| 2 | AIRism Cotton Oversized T-Shirt (Half-Sleeve) | UNISEX | 24.90 | 4.8 | 4,967 | 18 |
| 3 | Single Collar Short Blouson | UNISEX | 79.90 | 4.8 | 39 | 3 |
| 4 | HEATTECH Cashmere Blend T-Shirt (Extra Warm) | WOMEN | 24.90 | 4.6 | 500 | 10 |
| 5 | Warm Lined Pants | WOMEN | 49.90 | 4.6 | 34 | 4 |
| 6 | SUPIMA Cotton T-Shirt | UNISEX | 19.90 | 4.7 | 1,385 | 14 |
| 7 | Cashmere Sweater | MEN | 79.90 | 4.5 | 242 | 17 |
| 8 | HEATTECH Ultra Warm T-Shirt | WOMEN | 34.90 | 4.8 | 147 | 4 |
| 9 | Windproof Fleece Reversible Full-Zip Hoodie | WOMEN | 59.90 | 4.9 | 66 | 5 |
| 10 | Jersey Barrel Pants | UNISEX | 49.90 | 4.8 | 1,086 | 4 |

The widest colour range in the list was 21 colours on a single product.

## Things to know

- 14 of the 24 products had `prices.promo` set to `null`, and none had a promo price below the base price, so read the price as `promo or base`.
- The products come in the API's order, but there is no rank or score field in the response. Compare the order with `rating.count` before calling it a bestseller list.
- The call took several seconds, so cache it.

## Ideas

- Save the ranking daily and track which products move up.
- Join it with `/search` to see how ranked items sit in the price range of a category.
