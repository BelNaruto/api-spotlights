---
title: Track sales and discounts on any WooCommerce store with Python
image: /assets/woocommerce-sale-tracker-og.jpg
description: A Python script that lists the products on sale in any WooCommerce store, ranked by real discount, using the WooCommerce Stores Hub API on RapidAPI.
---

# Track sales on any WooCommerce store with Python

Point the script at any WooCommerce store, with no store keys needed, and get its on-sale products ranked by discount. It uses the [WooCommerce Stores Hub API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/woocommerce-stores-hub).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/on-sale` with `url` (the store address in any form), `page`, `perPage` (1-100) and filters such as `query` and `categoryId`. Every product has `prices` (`price`, `regularPrice`, `salePrice`, `discountPercent`), `onSale`, `stock` and `categories`. Full script: [`examples/woo_sale_tracker.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/woo_sale_tracker.py).

```python
data = call("/product/on-sale", url="dogoutfit.co.uk", perPage=10)
for p in data["products"]:
    pr = p["prices"]
    print(pr["discountPercent"], pr["price"], pr["regularPrice"], p["name"])
```

```bash
python woo_sale_tracker.py dogoutfit.co.uk 10
```

## Real output (20 Nov 2026)

The store dogoutfit.co.uk (a UK pet store, prices in GBP) has **214 products on sale**. The first 10 returned:

| Product | Price | Regular | Discount |
|---------|-------|---------|----------|
| Ellie-Bo Waterproof Memory Foam Orthopaedic Dog Bed (id 5454) | 14.99 | 33.79 | 56% |
| Ellie-Bo Waterproof Memory Foam Orthopaedic Dog Bed, 2X-Large, Green (id 5442) | 33.79 | 44.56 | 24% |
| Blueberry Pet 3M Reflective Dog Leads (ids 5655, 5612, 5572) | 11.99 | 15.39 | 22% |
| Bunty Deluxe Soft Washable Dog Basket Bed (id 5685) | 7.99 | 9.99 | 20% |
| Blueberry Pet Pink Flamingo Dog Lead (id 5531) | 11.99 | 13.41 | 11% |
| Blueberry Pet Classic Solid Dog Leads (id 5584) | 8.99 | 10.05 | 11% |
| Ellie-Bo Waterproof Memory Foam Orthopaedic Dog Bed (id 5456) | 32.94 | 33.79 | 3% |
| Jazooli Dog / Cat Safety Travel Seat Belt Restraint (id 5627) | 9.99 | 9.99 | none |

The last row is a quirk worth handling: the product was returned from the on-sale endpoint with `onSale: false` and the same price as the regular price, so it has no discount. That is why the script computes the discount from the prices and flags such items instead of trusting the list.

## Ideas

- Run it daily and alert when a product's `discountPercent` goes above 40.
- Pass `categoryId` to watch only one category.
