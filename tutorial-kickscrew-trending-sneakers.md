---
title: Build a trending sneakers leaderboard with demand score and sell-out risk (Python)
image: /assets/kickscrew-trending-sneakers-og.jpg
description: A short Python script that ranks sneakers in a collection by demand score and sell-out risk, using the KicksCrew Sneakers Data API on RapidAPI.
---

# Build a trending sneakers leaderboard in Python

This tutorial prints a "what is moving fast right now" leaderboard for any KicksCrew collection: lowest price, demand score, sell-out risk and how many sizes are still in stock. It uses the [KicksCrew Sneakers Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

Subscribe to the free plan on the [API page](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data), copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The script

The endpoint is `GET /v2/collections/{collection}/trending` with optional `limit` and `scanSize` parameters. Full script: [`examples/kickscrew_trending_sneakers.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/kickscrew_trending_sneakers.py).

```python
def trending(collection, limit=5):
    data = call(f"/v2/collections/{collection}/trending", limit=limit, scanSize=100)
    for i, p in enumerate(data["trending"], 1):
        sizes = f"{p['availableSizes']}/{p['totalSizes']}"
        print(i, p["title"], p["lowestPrice"], p["demandScore"], p["sellOutRisk"], sizes)
```

Run it:

```bash
python kickscrew_trending_sneakers.py air-jordan 5
```

## 3. Real output (20 Nov 2026)

The API scanned 100 products in the `air-jordan` collection and returned these five:

| # | Product | Lowest price (USD) | Demand score | Sell-out risk | Sizes in stock |
|---|---------|-------------------|--------------|---------------|----------------|
| 1 | (GS) Air Jordan 11 Retro 'Gamma Blue' 2025 378038-047 | 200.07 | 67 | HIGH | 9/27 |
| 2 | (GS) Air Jordan 1 Mid 'Ice Blue 2022' 555112-401 | 101.79 | 47 | MEDIUM | 8/15 |
| 3 | (GS) Air Jordan 11 'Legend Blue' 2024 378038-104 | 92.43 | 47 | MEDIUM | 8/15 |
| 4 | (GS) Air Jordan 4 Retro 'Thunder' 408452-017 | 201.24 | 47 | MEDIUM | 8/15 |
| 5 | Air Jordan 11 Retro 'Bred' 2012 378037-010 | 363.87 | 41 | MEDIUM | 11/32 |

The Gamma Blue 11 stands out: only 9 of 27 sizes left (66.67% sold through), so it is the only HIGH risk item. The response notes that `sellOutRisk` is a heuristic based on current size availability, not a guarantee of future stock.

## Ideas

- Run it daily and alert when an item moves from MEDIUM to HIGH.
- Change the collection handle to any brand or collection page on KicksCrew.
- Feed the product `handle` into the [regional pricing tutorial](tutorial-kickscrew-regional-price.html) to find the cheapest country.
