---
title: Build a US Treasury yield curve with spreads and an inversion check (Python)
image: /assets/investing-yield-curve-og.jpg
description: A short Python script that prints the US government bond yield curve, daily changes and the 10Y-2Y and 10Y-3M spreads, using the Investing.com Ultimate API on RapidAPI.
---

# Build a US Treasury yield curve in Python

Print the full government bond yield curve for a country, the daily change at every maturity, and the 10Y-2Y and 10Y-3M spreads that traders use to spot an inverted curve. It uses the [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /v2/markets/bonds` with optional `country` (code like `US`, `BR`, `DE`, a name or an id), `currency` and `language`. Each row has `name`, `yield`, `previous_close`, `change` and `change_percent`. Full script: [`examples/investing_yield_curve.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/investing_yield_curve.py).

```python
body = call("/v2/markets/bonds", country="US")
rows = {r["name"].split()[-1]: r for r in body["data"]}
spread_10y_2y = (rows["10Y"]["yield"] - rows["2Y"]["yield"]) * 100
```

```bash
python investing_yield_curve.py US
```

## Real output (20 Nov 2026, morning GMT)

13 maturities came back for the United States (yields in percent):

| Tenor | Yield | Previous close | Change |
|-------|-------|----------------|--------|
| 1M | 4.110 | 4.114 | -0.005 |
| 2M | 4.184 | 4.191 | -0.007 |
| 3M | 4.245 | 4.260 | -0.015 |
| 4M | 4.344 | 4.352 | -0.008 |
| 6M | 4.439 | 4.464 | -0.025 |
| 1Y | 4.538 | 4.595 | -0.058 |
| 2Y | 4.687 | 4.779 | -0.092 |
| 3Y | 4.723 | 4.818 | -0.095 |
| 5Y | 4.771 | 4.866 | -0.095 |
| 7Y | 4.853 | 4.944 | -0.091 |
| 10Y | 4.963 | 5.050 | -0.087 |
| 20Y | 5.389 | 5.451 | -0.062 |
| 30Y | 5.348 | 5.401 | -0.053 |

Computed from those numbers: the **10Y-2Y spread is +27.6 bp** and the **10Y-3M spread is +71.8 bp**, so the curve is upward sloping (not inverted). Yields fell at every maturity, most at the 2Y to 7Y part of the curve. The 20Y yield sits slightly above the 30Y, a small hump at the long end.

## Ideas

- Run it for `DE`, `JP` or `BR` and compare curves.
- Store the 10Y-2Y spread daily and alert when it crosses zero.
