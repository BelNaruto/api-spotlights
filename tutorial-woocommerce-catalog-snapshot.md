---
title: Get a catalog snapshot of any WooCommerce store: size, prices and categories (Python)
image: /assets/woocommerce-catalog-snapshot-og.jpg
description: A Python script that summarises any WooCommerce store's newest products (catalog size, price range, stock and categories) using the WooCommerce Stores Hub API on RapidAPI.
---

# Get a catalog snapshot of any WooCommerce store

Useful for competitor research: how big is the catalog, how are the newest products priced, and which categories are growing. It uses the [WooCommerce Stores Hub API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/woocommerce-stores-hub).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/newest` with the same filters as the other product lists. The `pagination` block gives the full catalog size. Full script: [`examples/woo_catalog_snapshot.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/woo_catalog_snapshot.py).

```python
data = call("/product/newest", url="dogoutfit.co.uk", perPage=20)
print(data["pagination"]["total"], "products in the catalog")
prices = sorted(p["prices"]["price"] for p in data["products"])
```

```bash
python woo_catalog_snapshot.py dogoutfit.co.uk
```

## Real output (20 Nov 2026)

For dogoutfit.co.uk:

- **648 products** in the catalog (33 pages of 20)
- Newest 20 products priced in GBP: minimum 1.20, median 11.99, maximum 33.79 (average 12.19)
- 9 of the 20 are on sale, and all 20 are in stock
- Categories among the newest 20: Dog Harnesses (10, also listed under the parent category Harnesses), Memory foam offcuts (6), Dog Beds (4)

Combining it with the [sale tracker](tutorial-woocommerce-sale-tracker.html): 214 of the 648 products (about a third) are on sale right now.

## Ideas

- Take a snapshot every week and track catalog growth.
- Page through `/product/all` with `perPage=100` to build the full price list.
