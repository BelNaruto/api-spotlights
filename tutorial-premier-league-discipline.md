---
title: Compare the discipline record of Premier League teams with Python
image: /assets/premier-league-discipline-og.jpg
description: A Python script that adds up yellow and red cards per team and finds the most booked player, using the English Premiere League API on RapidAPI.
---

# Compare Premier League discipline records with Python

Pass a season and a few team ids and the script prints each team's yellow cards, red cards, discipline points and most booked player. It uses the [English Premiere League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /team/statistic/discipline` with `teamId` and `season` (the first year of the season, so `2025` is 2025-26). The response has `team`, `requestedSeason`, `currentSeason` and `results`, a list of players. Each player has `displayName`, `shortName`, `jersey` and `statistics` with `appearances`, `yellowCards`, `redCards` and `points`. Get team ids from the Team List endpoint. Full script: [`examples/premier_league_discipline.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/premier_league_discipline.py).

```python
body = call("/team/statistic/discipline", teamId="364", season="2025")
for p in body["results"]:
    print(p["shortName"], [(s["name"], s["value"]) for s in p["statistics"]])
```

```bash
python premier_league_discipline.py 2025 364 359 382
```

## Real output (20 Nov 2026)

Season 2025-26 for Liverpool (364), Arsenal (359) and Manchester City (382):

| Team | Players | Yellow | Red | Points | Most booked |
|------|---------|--------|-----|--------|-------------|
| Liverpool | 21 | 49 | 1 | 52 | D. Szoboszlai (8 yellow, 1 red) |
| Arsenal | 19 | 35 | 0 | 35 | R. Calafiori (5 yellow) |
| Manchester City | 22 | 62 | 0 | 62 | B. Silva (10 yellow) |

Discipline `points` is one point per yellow and three per red: Liverpool's 52 is 49 + 3.

## Things to know

- The `team` block always describes the current season. Liverpool's `recordSummary` was 5-3-2 and its standing "4th" (2026-27), while the player rows were for the requested 2025-26 season.
- The playground default for `season` is 2023, so pass the season explicitly.
- `foulsCommitted` and `foulsSuffered` are not in this endpoint. Use the scoring statistics endpoint (next tutorial) for fouls.

## Ideas

- Loop over the Team List endpoint to build a full league discipline table.
- Sort players by points to see who is closest to a suspension.
