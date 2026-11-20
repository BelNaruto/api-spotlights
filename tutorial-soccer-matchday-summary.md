---
title: Summarise a whole day of world football in Python: results, goals and biggest wins
image: /assets/soccer-matchday-summary-og.jpg
description: A Python script that summarises every football match played on a date (results, goals per game, home/draw/away split and biggest margins) using the Soccer Live Info API on RapidAPI.
---

# Summarise a whole day of football in Python

One request returns every match played on a date, grouped by competition. This script turns it into a match day report. It uses the [Soccer / Football Live Info API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/soccer-football-live-info).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /matches` with `date` (`YYYY-MM-DD`) and optional filters `tz`, `status`, `competitionId` and `teamId`. The response is a list of competitions, each with its matches, scores and status. Full script: [`examples/soccer_matchday_summary.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/soccer_matchday_summary.py).

```python
comps = call("/matches", date="2026-11-14")
matches = [m for c in comps for m in c["matches"]]
```

```bash
python soccer_matchday_summary.py 2026-11-14
```

## Real output for Saturday 14 Nov 2026

- **562 matches in 89 competitions**: 544 finished, 17 postponed, 1 cancelled
- **1,650 goals in 544 finished matches**, which is 3.03 goals per match
- 250 home wins, 118 draws and 176 away wins
- Busiest competitions: Coupe de France (51 matches), Oberliga in Germany (51), FA Trophy in England (40), Northern Premier League (28), U19 Euro qualifiers (26)
- 12 red cards in total

The biggest margins of the day:

| Result | Competition |
|--------|-------------|
| Norway U17 11-0 Malta U17 | European Championship U17 Qualification |
| FC Kilia Kiel 8-1 VfR Neumuenster | Oberliga (Germany) |
| ES Buxerolles 0-7 Sable FC | Coupe de France |
| RW Wittlich 7-0 SV Auersmacher | Oberliga (Germany) |
| Kazakhstan U17 7-0 Austria U17 | European Championship U17 Qualification |

The response for this date is large (about 500 KB, 9.5 seconds on this run), so cache it if you call it often.

## Ideas

- Filter with `competitionId` to build a report for one league.
- Run it every Monday for the weekend and post the headline numbers.
