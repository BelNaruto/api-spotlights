---
title: Find the biggest Black Friday savings on Macy's with Python
image: /assets/macys-black-friday-deals-og.jpg
description: A Python script that pulls Macy's deal products and ranks them by dollars saved, using the Macy's API on RapidAPI.
---

# Find the biggest Black Friday savings on Macy's

Pull Macy's current deal products and sort them by how many dollars you actually save. It uses the [Macy's API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/macys4).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /api/deals/products` with `page`, `perPage`, `sortBy`, `filters`, `currencyCode` and `regionCode`. Product names can contain HTML entities (for example `Lanc&ocirc;me`), so the script runs them through `html.unescape`. Full script: [`examples/macys_black_friday_deals.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/macys_black_friday_deals.py).

```python
result = call("/api/deals/products", page=1, perPage=10)
for p in result["products"]:
    s = p["priceSummary"]
    print(s["regular"] - s["current"], s["percentOff"], s["promotion"], p["detail"]["name"])
```

```bash
python macys_black_friday_deals.py 10
```

## Real output (20 Nov 2026)

The API reported 188,000 deal products. The first 10, ranked by dollars saved (accents removed for plain text):

| Brand | Product | Now | Was | Saved | Off | Promotion |
|-------|---------|-----|-----|-------|-----|-----------|
| COACH | Soft Empire Small Leather Satchel Bag 21 | $195.00 | $325.00 | $130.00 | 40% | Black Friday Deal |
| Charter Club | Women's 100% Cashmere Quarter-Zip Sweater | $69.99 | $199.00 | $129.01 | 65% | Black Friday Deal |
| COACH | Jet Small Leather Slim Shoulder Bag | $221.25 | $295.00 | $73.75 | 25% | Black Friday Deal |
| Burberry | 3-Piece Goddess Eau de Parfum Spray Gift Set | $136.50 | $195.00 | $58.50 | 30% | Black Friday Deal |
| Lacoste | Men's Pima Regular-Fit Cotton Polo Shirt | $55.00 | $110.00 | $55.00 | 50% | Black Friday Deal |
| Created For Macy's | 25-Days of Beauty Advent Calendar Set | $59.40 | $99.00 | $39.60 | 40% | Black Friday Deal |
| Lancome | Renergie C.R.x. Triple Serum Retinol | $43.80 | $73.00 | $29.20 | 40% | Today Only |
| Steve Madden | Animal Print 3-Piece Earwarmer Headbands and Gloves | $19.99 | $48.00 | $28.01 | 58% | Today Only |
| Lancome | Genifique Ultimate Recovery Face Serum | $39.00 | $65.00 | $26.00 | 40% | Today Only |
| Steve Madden | 3-Pack Chenille Magic Gloves Set | $19.99 | $40.00 | $20.01 | 50% | Today Only |

The biggest dollar saving is the COACH satchel ($130.00), with the Charter Club cashmere sweater a dollar behind ($129.01) but the deepest percentage cut at 65%.

## Ideas

- Use `sortBy` and `filters` to restrict deals to one brand or category.
- Each response is large (about 366 KB for 10 products), so keep `perPage` small and cache the results.
