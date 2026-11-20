---
title: Build the Champions League league-phase table with Python
image: /assets/uefa-league-phase-table-og.jpg
description: A Python script that prints the full 36-team Champions League league-phase table with qualification zones, using the UEFA Champions League API on RapidAPI.
---

# Build the Champions League league-phase table with Python

The Champions League has one 36-team table. This script fetches it for any season and prints each team's record, goal difference and qualification zone. It uses the [UEFA Champions League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/uefa-champions-league1).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /standingsv2` with `season` (the starting year, for example `2025`). The table is in `children[0].standings.entries`. Each entry has a `team`, a `note.description` (the zone) and a `stats` list you look up by name: `rank`, `gamesPlayed`, `wins`, `ties`, `losses`, `pointDifferential`, `points`, `pointsFor` and `pointsAgainst`. Full script: [`examples/uefa_league_phase_table.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/uefa_league_phase_table.py).

```python
data = call("/standingsv2", season=2025)
for e in data["children"][0]["standings"]["entries"]:
    print(stat(e, "rank"), e["team"]["displayName"], stat(e, "points"), e["note"]["description"])
```

```bash
python uefa_league_phase_table.py 2025
```

## Real output (20 Nov 2026)

Season `2025` returned the finished **2025-26 league phase: 36 teams, 144 matches, 487 goals (3.38 per match)**. Zones: 8 qualify for the round of 16, 8 are seeded for the playoffs, 8 unseeded, 12 eliminated.

| # | Team | W | D | L | GD | Pts | Zone |
|---|------|---|---|---|----|-----|------|
| 1 | Arsenal | 8 | 0 | 0 | +19 | 24 | Round of 16 |
| 2 | Bayern Munich | 7 | 0 | 1 | +14 | 21 | Round of 16 |
| 3 | Liverpool | 6 | 0 | 2 | +12 | 18 | Round of 16 |
| 4 | Tottenham Hotspur | 5 | 2 | 1 | +10 | 17 | Round of 16 |
| 5 | Barcelona | 5 | 1 | 2 | +8 | 16 | Round of 16 |
| 9 | Real Madrid | 5 | 0 | 3 | +9 | 15 | Playoffs, seeded |
| 24 | Benfica | 3 | 0 | 5 | -2 | 9 | Playoffs, unseeded |
| 36 | Kairat Almaty | 0 | 1 | 7 | -15 | 1 | Eliminated |

Real Madrid has a better goal difference (+9) than the teams ranked 5 to 8, but ranks 9th because points come first. Sorting by points then goal difference is how to read the table.

## Things to know

- The endpoint's documented default is `season=2023`, which predates the league-phase format. Always pass the season explicitly.
- Use the `note.description` text as the zone label rather than hard-coding rank cut-offs.

## Ideas

- Draw the table as an image for a social post.
- Compare `pointsFor` and `pointsAgainst` to find the best attack and defence.
