---
title: Build a live metals dashboard with gold, silver and copper futures (Python)
image: /assets/investing-metals-dashboard-og.jpg
description: A Python script that prints live metals futures (gold, silver, copper, aluminium and more) sorted by daily move, using the Investing.com Ultimate API on RapidAPI.
---

# Build a live metals dashboard in Python

Pull live futures prices for precious and industrial metals and sort them by today's move. It uses the [Investing.com Ultimate API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/investing-com-ultimate-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /v2/markets/commodities` with a `group` parameter (the default is `metals`), plus optional `language` and `currency`. The response contains blocks of rows, each with `name`, `last`, `change_percent` and `contract_month`. Full script: [`examples/investing_metals_dashboard.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/investing_metals_dashboard.py).

```python
body = call("/v2/markets/commodities", group="metals")
for block in body["data"]:
    for r in block["rows"]:
        print(r["name"], r["last"], r["change_percent"], r["contract_month"])
```

```bash
python investing_metals_dashboard.py metals
```

## Real output (20 Nov 2026)

The first block (real-time streaming futures) returned 11 instruments:

| Metal | Last | Change | Contract |
|-------|------|--------|----------|
| Gold | 3,580 | -2.86% | Dec 26 |
| Copper | 5.5148 | -2.11% | Dec 26 |
| Silver | 42.14 | -5.00% | Dec 26 |
| Palladium | 911 | -0.81% | Dec 26 |
| Platinum | 1,307.1 | -3.00% | Jan 27 |
| Aluminium | 2,839.65 | -1.00% | - |
| Zinc | 3,496.1 | -1.90% | - |
| Lead | 1,856.3 | -0.64% | - |
| Nickel | 15,448.5 | -0.91% | - |
| Tin | 42,855 | -5.02% | - |
| Copper (second listing) | 12,193.85 | -2.33% | - |

Two more blocks came back: delayed futures (US Steel Coil, Micro Silver, Micro Gold, Aluminum, Uranium 90.25, Iron Ore 62% 90.86) and one Eurex quote (Xetra-Gold 107.95, -1.54%). It was a red day: tin (-5.02%) and silver (-5.00%) fell the most.

Note that the API does not report a currency for each row (the response says so in its `currency_note`); values are in each instrument's own currency. Copper appears twice with different units, so check the `name` and contract before comparing.

## Ideas

- Compute the gold/silver ratio (3,580 / 42.14 is about 85) and chart it daily.
- Try other `group` values for energy or agricultural commodities.
