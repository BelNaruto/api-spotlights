---
title: Find the cheapest country to buy a sneaker with live FX conversion (Python)
description: A Python script that compares one sneaker's price across 10 country storefronts, converted to USD, using the KicksCrew Sneakers Data API on RapidAPI.
---

# Find the cheapest country to buy a sneaker

The same sneaker can have very different prices depending on the storefront. This tutorial compares one product across 10 countries, converts everything into one currency with live exchange rates, and shows the cheapest and priciest market. It uses the [KicksCrew Sneakers Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/kickscrew-sneakers-data).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /v2/products/{handle}/regional-pricing` with optional `baseCurrency` and `countries` (up to 15, comma separated). The `handle` is the last part of a kickscrew.com product URL. Full script: [`examples/kickscrew_regional_price.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/kickscrew_regional_price.py).

```python
d = call(f"/v2/products/{handle}/regional-pricing",
         baseCurrency="USD", countries="US,GB,CA,AU,DE,FR,JP,KR,SG,HK")
for p in d["prices"]:
    print(p["country"], p["amount"], p["currency"], p["usdEquivalent"])
print(d["cheapestCountry"], d["priciestCountry"], d["maxSavingsPercent"])
```

```bash
python kickscrew_regional_price.py gs-air-jordan-11-retro-gamma-blue-2025-378038-047
```

## Real output (20 Nov 2026)

Product: (GS) Air Jordan 11 Retro 'Gamma Blue' 2025. FX rates as of 20 Nov 2026 00:02 UTC.

| Country | Local price | USD equivalent |
|---------|-------------|----------------|
| HK | 1341 HKD | 170.95 |
| JP | 30200 JPY | 189.05 |
| KR | 255000 KRW | 191.59 |
| US | 200.07 USD | 200.07 |
| SG | 262 SGD | 202.97 |
| AU | 317 AUD | 211.51 |
| CA | 305 CAD | 212.91 |
| FR | 224.95 EUR | 246.99 |
| DE | 228.95 EUR | 251.39 |
| GB | 192 GBP | 251.85 |

Cheapest is **Hong Kong**, priciest is **Great Britain**, with a maximum saving of **32.12%**. The UK sticker price (192) looks lower than the US one (200.07) until you convert it: in dollars it is the most expensive market.

## Ideas

- Pair it with the [trending leaderboard](tutorial-kickscrew-trending-sneakers.html) to price-check every hot sneaker.
- Compare your shipping and import costs against the savings before buying abroad.
