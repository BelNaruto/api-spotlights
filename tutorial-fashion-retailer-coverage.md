---
title: Check which fashion retailers are live before you search, with Python
image: /assets/fashion-retailer-coverage-og.jpg
description: A Python script that lists every retailer supported by the Fashion Product API and its live status, so your app can skip the ones that are down.
---

# Check retailer coverage before you search

Some retailers are harder to reach than others. This script asks the Fashion Product API which of its 16 retailers are available, so you can show or hide them in your own app. It uses the [Fashion Product API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/fashion-product-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /retailers` with no parameters. It returns `data.count` and `data.retailers`, each with `retailer` (the id), `label`, `origin` and `status`. Full script: [`examples/fashion_retailer_coverage.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/fashion_retailer_coverage.py).

```python
data = call("/retailers")
for r in data["retailers"]:
    print(r["status"], r["label"], r["origin"])
```

```bash
python fashion_retailer_coverage.py
```

## Real output (20 Nov 2026)

**16 retailers**: 14 `available`, 1 `unavailable` (Farfetch) and 1 `unverified` (SHEIN).

| Status | Retailers |
|--------|-----------|
| available | ASOS, Zara, H&M, Fashion Nova, SKIMS, Public Desire, Oh Polly, Motel Rocks, Killstar, Lucy & Yak, Victoria Beckham, French Connection, Represent, Steve Madden |
| unavailable | Farfetch |
| unverified | SHEIN |

Note that `status` is a general flag. In a live `jacket` search on the same day SKIMS was marked `available` here but returned no products, so also read `data.retailers[].available` in search responses.

## Ideas

- Call it once an hour and show only `available` retailers in a filter dropdown.
- Use `origin` to link each result back to the retailer's own site.
