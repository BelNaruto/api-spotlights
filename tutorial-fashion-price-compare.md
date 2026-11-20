---
title: Compare fashion prices across ASOS, Zara, H&M and 10 more retailers with Python
image: /assets/fashion-price-compare-og.jpg
description: A Python script that searches one term across many fashion retailers in a single call and compares median and average prices, using the Fashion Product API on RapidAPI.
---

# Compare fashion prices across retailers with Python

One request searches ASOS, Zara, H&M, Fashion Nova, Steve Madden and more at the same time. The script groups the results by retailer and prints the median and average price. It uses the [Fashion Product API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/fashion-product-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /products/search/all` with `q`. The response has `data.count`, `data.results` (each with `retailer`, `name`, `brand`, `price` as `{amount, currency, text}`, `image`, `availability`, `sourceUrl`) and `data.retailers` (one entry per retailer with `available`, `count` and a `reason` when it returned nothing). Full script: [`examples/fashion_price_compare.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/fashion_price_compare.py).

```python
data = call("/products/search/all", q="jacket")
for p in data["results"]:
    print(p["retailer"], p["price"]["amount"], p["price"]["currency"], p["name"])
```

```bash
python fashion_price_compare.py jacket
```

## Real output (20 Nov 2026)

The query `jacket` returned **252 products from 13 retailers** in about 9.5 seconds (a 105 KB response). Prices are in each retailer's own currency.

| Retailer | Items | Median | Average | Currency |
|----------|-------|--------|---------|----------|
| Fashion Nova | 24 | 21.99 | 22.83 | USD |
| H&M | 24 | 47.49 | 46.41 | USD |
| Killstar | 24 | 50.75 | 59.54 | GBP |
| Motel Rocks | 24 | 56.00 | 56.67 | GBP |
| Lucy & Yak | 2 | 46.00 | 46.00 | GBP |
| Public Desire | 12 | 82.99 | 70.75 | USD |
| ASOS | 24 | 109.00 | 104.46 | USD |
| Zara | 24 | 119.00 | 119.46 | USD |
| Steve Madden | 20 | 129.00 | 116.70 | USD |
| French Connection | 24 | 200.00 | 207.20 | USD |
| Oh Polly | 24 | 181.50 | 168.50 | USD |
| Represent | 24 | 522.50 | 680.38 | USD |
| Victoria Beckham | 2 | 1,670.00 | 1,670.00 | USD |

Two retailers asked for returned nothing: SHEIN (`available: false`, with a reason saying its keyword search is best-effort) and SKIMS (`available: false`, count 0). The script prints these so a missing retailer is never silent.

## Things to know

- Prices are not converted: three retailers answer in GBP and the rest in USD, so compare within a currency or convert first.
- Small result sets (Lucy & Yak and Victoria Beckham have 2 items each) make the median unreliable. Check the `Items` column.
- Responses are large and take several seconds, so cache by query.

## Ideas

- Run it for a list of terms (`jacket`, `sneakers`, `dress`) and chart the median per retailer.
- Save the results daily to spot price drops on specific products using `id` (for example `asos:210818451`).
