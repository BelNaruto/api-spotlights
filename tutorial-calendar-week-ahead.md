---
title: Build a week-ahead economic calendar of high-impact market events (Python)
description: A short Python script that lists the high-impact economic events for the coming week, grouped by day with forecast and previous values, using the Trader Calendar API on RapidAPI.
---

# Build a week-ahead economic calendar in Python

Print the high-impact economic events for any date range, grouped by day, with forecast and previous values. It uses the [Trader Calendar API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/trader-calendar-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /calendar`. Dates use `dd/mm/yyyy`, and `from_date` and `to_date` must be sent together. `importances` accepts `low`, `medium`, `high`. Full script: [`examples/calendar_week_ahead.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/calendar_week_ahead.py).

```python
events = call("/calendar", from_date="23/11/2026", to_date="27/11/2026",
              importances="high", countries="united states,euro zone")
for e in events:
    print(e["date"], e["time"], e["event"], e["forecast"], e["previous"])
```

```bash
python calendar_week_ahead.py 23/11/2026 27/11/2026
```

## Real output (queried 20 Nov 2026)

The API returned 10 high-impact events (times in GMT):

| Date | Time | Event | Forecast | Previous |
|------|------|-------|----------|----------|
| 23/11 | 14:45 | S&P Global Services PMI (Nov) | - | 56.1 |
| 23/11 | 14:45 | S&P Global Manufacturing PMI (Nov) | - | 54.9 |
| 24/11 | 15:00 | CB Consumer Confidence (Nov) | 92.0 | 91.7 |
| 25/11 | 13:30 | Core PCE Price Index (MoM) (Oct) | 0.3% | 0.3% |
| 25/11 | 13:30 | Core PCE Price Index (YoY) (Oct) | 3.2% | 3.1% |
| 25/11 | 13:30 | GDP (QoQ) (Q3) | 3.4% | 2.2% |
| 25/11 | 13:30 | Durable Goods Orders (MoM) (Oct) | 0.0% | 1.9% |
| 25/11 | 13:30 | Initial Jobless Claims | - | 203K |
| 25/11 | 15:00 | New Home Sales (Oct) | 670K | 676K |
| 25/11 | 15:30 | Crude Oil Inventories | - | 3.380M |

Wednesday 25 November is the day to watch: PCE inflation, Q3 GDP, durable goods and jobless claims all land at 13:30 GMT. Each event also carries the `actual` value (empty until the release), an `event_id` and an investing.com `url`.

## Ideas

- Pass `time_zone="GMT +1:00"` to get local times (it also changes where each day starts and ends).
- Schedule it every Sunday and send the output to Slack or email.
