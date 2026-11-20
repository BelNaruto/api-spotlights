---
title: Scan SHEIN for the deepest discounts and best-rated items with Python
image: /assets/shein-sale-scanner-og.jpg
description: A Python script that searches SHEIN, summarises prices and discounts, and ranks the deepest cuts with their ratings, using the Shein Data API on RapidAPI.
---

# Scan SHEIN for the deepest discounts with Python

Search SHEIN for any keyword and get a short sale report: price range, share of discounted items, and the five deepest discounts with their ratings. It uses the [Shein Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/shein-data-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /search/products` with `query`, `country` (a 2-letter code such as US, GB or FR), `limit` (1 to 120), `page`, `sort` and `min_price`. The response has `data.total` and `data.products`. Each product has `name`, `category`, `rating` (`average`, `count`), `in_stock`, `quick_ship` and a `price` object with `sale`, `retail` and `discount_percent`. Full script: [`examples/shein_sale_scanner.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/shein_sale_scanner.py).

```python
data = call("/search/products", query="dress", country="US", limit=20)
for p in data["products"]:
    print(p["price"]["discount_percent"], p["price"]["sale"]["display"], p["name"][:40])
```

```bash
python shein_sale_scanner.py dress US
```

## Real output (20 Nov 2026)

A search for `dress` in the US store reported **16,283 results** and returned 20 products. Prices ran from **11.81 to 29.40 USD** (median about 16). All 20 were discounted, with an average of **26.1%** and a maximum of **40%**. All 20 were in stock and 3 offered quick shipping. The products came from six categories, mostly Women Mini Dresses (12).

| Discount | Retail | Sale | Rating | Product |
|----------|--------|------|--------|---------|
| 40% | $32.49 | $19.47 | 4.81 | Travachic Women's Pleated Emerald Green |
| 38% | $22.79 | $14.15 | 4.76 | SaltGleam Women's Summ... |
| 34% | $20.29 | $13.42 | 4.63 | Aloruh Women's Solid Color One-Shoulder |

The discount percentage matched `1 - sale / retail` for all 20 products.

## Things to know

- Only the first page is available. The response says `total_pages: 815` but also `pagination_supported: false` and `snapshot_pages_available: 1`, so `page=2` is not a reliable way to get more.
- Review counts are capped: four products show `count_display: "1000+"` with a count of 1001. Do not rank by count among those.
- Prices come with a `usd_amount` field, so you can compare stores in other countries in one currency.
- `data_level` is `snapshot`. Use the price endpoint (next tutorial) for details on a single product.

## Ideas

- Run it for several keywords and chart the average discount per category.
- Save each run and alert when a product drops below a price.
