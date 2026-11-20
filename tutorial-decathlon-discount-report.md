---
title: Find the biggest discounts and low stock in Decathlon new arrivals with Python
image: /assets/decathlon-discount-report-og.jpg
description: A Python script that reads a Decathlon collection with the Decathlon API on RapidAPI and shows discounts by product and brand and how many sizes are in stock.
---

# Find discounts and low stock in Decathlon new arrivals

The [Decathlon API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/decathlon-api) returns Decathlon store products with their sizes, prices and stock. This script reads the `new-arrivals` collection and answers two questions: what is on sale and by how much, and which products are running out of sizes.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /collection/products` with `collectionsHandle`, `page` and `country`. Each product has `variants`, one per size, with `price`, `compare_at_price` and `available`. The script takes the lowest price and the highest compare-at price of each product, computes the discount, and counts the sizes that are available. Full script: [`examples/decathlon_discount_report.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/decathlon_discount_report.py).

```python
products = call("/collection/products", collectionsHandle="new-arrivals", page=1, country="us")
```

```bash
python decathlon_discount_report.py new-arrivals
```

## Real output (20 Nov 2026)

Product titles are shortened here to keep the lines short.

```
30 products, 21 with a compare_at_price above the price
Average discount on those: 32%

Biggest discounts:
  -46%   70.00 (was 130.00)  Kiprun Kipsummit Men's Trail R
  -46%   70.00 (was 130.00)  Kiprun Kipsummit Women's Trail
  -38%  100.00 (was 160.00)  Kiprun 15L Ultra Trail Running
  -33%   20.00 (was 29.99)  Forclaz Adult MT500 Touchscree
  -33%   60.00 (was 89.99)  Quechua MH500 22L Lightweight 

By brand:   products  on sale  sizes in stock
  Kiprun           10        7  99/123
  Simond            6        6  36/36
  Quechua           6        3  12/13
  Decathlon         6        3  6/6
  Forclaz           2        2  10/16

Products with less than half the sizes in stock: 2
  1/11  Kiprun Kipstorm Elite Men's Carbon
  4/10  Kiprun Kipstorm Elite Women's Carb
```

Seven of the ten Kiprun products are on sale, and the two Kipsummit trail shoes have the deepest cut at 46%. The Kipstorm Elite men's carbon shoe has only 1 of 11 sizes left.

## Things to know

- `price` and `compare_at_price` are text, so convert them to numbers. A missing compare-at price is `null`, and some products use `0`.
- One call returns 30 products and takes about 3.6 s. Use `page` to read more.
- The same product can appear more than once in the collection. In this run 24 of the 30 titles were different.
- The discount uses the highest compare-at price of any size, so a product with several prices can show a higher discount than a single size has.

## Ideas

- Run it every day and save the lowest price per product to find real price drops.
- Send yourself a message when a product you follow falls below 3 sizes in stock.
