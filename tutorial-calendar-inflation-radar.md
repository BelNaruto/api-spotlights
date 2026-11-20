---
title: Build an inflation and central bank radar across countries (Python)
image: /assets/calendar-inflation-radar-og.jpg
description: A Python script that tracks inflation releases and central bank events across the US, euro zone, UK and Japan using the Trader Calendar API on RapidAPI.
---

# Build an inflation and central bank radar in Python

Filter the economic calendar down to what moves rates: inflation data and central bank events, across several countries at once. It uses the [Trader Calendar API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/trader-calendar-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

Same `GET /calendar` endpoint, with `categories`, `importances` and `countries` filters. Country names come from `GET /api/countries`; use `euro zone` for ECB and eurozone data. Full script: [`examples/calendar_inflation_radar.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/calendar_inflation_radar.py).

```python
events = call("/calendar", from_date="23/11/2026", to_date="04/12/2026",
              importances="medium,high", categories="inflation,central_banks",
              countries="united states,euro zone,united kingdom,japan")
```

```bash
python calendar_inflation_radar.py 23/11/2026 04/12/2026
```

## Real output (queried 20 Nov 2026)

22 events came back: US, Japan, euro zone and UK. The high-impact inflation releases in the window:

| Date | Time (GMT) | Country | Event | Forecast | Previous |
|------|-----------|---------|-------|----------|----------|
| 25/11 | 13:30 | United States | Core PCE Price Index (MoM) (Oct) | 0.3% | 0.3% |
| 25/11 | 13:30 | United States | Core PCE Price Index (YoY) (Oct) | 3.2% | 3.1% |
| 01/12 | 10:00 | Euro zone | CPI (YoY) (Nov) | - | 4.0% |
| 01/12 | 15:00 | United States | ISM Manufacturing Prices (Nov) | - | 75.2 |
| 03/12 | 15:00 | United States | ISM Non-Manufacturing Prices (Nov) | - | 73.0 |

Medium-impact items in the same window include Japan's BoJ Core CPI (previous 2.5%) and Tokyo Core CPI (previous 2.6%), Michigan inflation expectations on 4 December (1-year 4.7%, 5-year 3.5%), the ECB account of its last meeting (26 Nov), the BoE Financial Stability Report (26 Nov) and the Fed's Beige Book (25 Nov).

Note that the `central_banks` category is broad: it also contained the EU Leaders Summit and an OPEC meeting, so filter by event name if you only want rate-setting meetings.

## Ideas

- Add `united kingdom` CPI and `canada` to the country list.
- Highlight rows where `forecast` is above `previous` to flag possible upside inflation surprises.
