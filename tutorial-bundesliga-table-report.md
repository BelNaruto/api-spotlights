---
title: Print the Bundesliga table with European places and relegation using Python
image: /assets/bundesliga-table-report-og.jpg
description: A Python script that prints the full Bundesliga table, checks the points arithmetic and shows the European and relegation notes, using the German Bundesliga API on RapidAPI.
---

# Print the Bundesliga table with Python

Fetch a full Bundesliga season, print the table with goals and notes (Champions League, Europa League, relegation), and check that every team's points add up. It uses the [German Bundesliga API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/german-bundesliga-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /standings` with `year` (the first year of the season, so `2025` is 2025-26). The table is at `standings.children[0].standings.entries`. Each entry has a `team`, a `note` for qualification or relegation places, and a `stats` list with `rank`, `gamesPlayed`, `wins`, `ties`, `losses`, `pointsFor`, `pointsAgainst`, `pointDifferential`, `points` and `deductions`. Full script: [`examples/bundesliga_table_report.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/bundesliga_table_report.py).

```python
league = call("/standings", year="2025")["standings"]
for e in league["children"][0]["standings"]["entries"]:
    s = {x["name"]: x["value"] for x in e["stats"]}
    print(int(s["rank"]), e["team"]["displayName"], int(s["points"]))
```

```bash
python bundesliga_table_report.py 2025
```

## Real output (20 Nov 2026)

The 2025-26 season has 18 teams and 34 games each. The top and bottom of the table:

| # | Team | W | D | L | GF | GA | GD | Pts | Note |
|---|------|---|---|---|----|----|----|-----|------|
| 1 | Bayern Munich | 28 | 5 | 1 | 122 | 36 | +86 | 89 | Champions League |
| 2 | Borussia Dortmund | 22 | 7 | 5 | 70 | 34 | +36 | 73 | Champions League |
| 3 | RB Leipzig | 20 | 5 | 9 | 66 | 47 | +19 | 65 | Champions League |
| 4 | VfB Stuttgart | 18 | 8 | 8 | 71 | 49 | +22 | 62 | Champions League |
| 5 | TSG Hoffenheim | 18 | 7 | 9 | 65 | 52 | +13 | 61 | Europa League |
| 6 | Bayer Leverkusen | 17 | 8 | 9 | 68 | 47 | +21 | 59 | Europa League |
| 16 | VfL Wolfsburg | 7 | 8 | 19 | 45 | 69 | -24 | 29 | Relegation playoff |
| 17 | 1. FC Heidenheim 1846 | 6 | 8 | 20 | 41 | 72 | -31 | 26 | Relegation |
| 18 | St. Pauli | 6 | 8 | 20 | 29 | 60 | -31 | 26 | Relegation |

Across the league there were **990 goals in 306 matches, 3.24 per match**. Goals for equal goals against (990 each), goal difference matched on every row, and `3 × wins + draws` matched `points` for all 18 teams.

## Things to know

- The playground default for `year` is 2023, so pass the season you want.
- Heidenheim and St. Pauli have identical points and goal difference (26 points, -31), and the API still lists them as 17 and 18.
- The `ppg` stat was 0 for Bayern Munich, so work out points per game yourself.
- Team names are not consistent in style: "Mainz", "FC Cologne" and "1. FC Union Berlin" all appear.
- The `seasons` list holds 25 seasons, from 2002/03 to 2026-27.

## Ideas

- Compare the final table of several seasons and chart the champion's points.
- Turn the notes into a "who goes where" summary for a fan site.
