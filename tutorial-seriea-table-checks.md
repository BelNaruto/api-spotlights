---
title: Check a Serie A table for data errors with Python
image: /assets/seriea-table-checks-og.jpg
description: A Python script that tests the Serie A table from the Serie A API on RapidAPI for wrong points, game counts, goal totals and empty fields before you build on it.
---

# Check the Serie A table before you build on it

A table is easy to test, because the numbers must add up. This script reads the table from the [Serie A API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/serie-a-api1) and runs a few checks.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /tables?season=2025` and tests: points equal 3 x wins + draws, wins + draws + losses equal games played, and the goals scored by all teams equal the goals conceded. It also counts teams where `ppg` is 0 and shows the zone labels. Full script: [`examples/seriea_table_checks.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/seriea_table_checks.py).

```python
gf, ga = sum(s["pointsFor"] for s in table), sum(s["pointsAgainst"] for s in table)
```

```bash
python seriea_table_checks.py 2025
```

## Real output (20 Nov 2026)

```
2025-26 Italian Serie A: 20 teams

Teams with wrong points or games: 0
Goals scored 922, conceded 922 -> equal
Games per team: [38]
Teams with ppg = 0 in the API: 20 of 20
Teams with a deduction: 0
Zones: {'Champions League': 4, 'Europa League': 2, 'Conference League qualifying': 1, '(none)': 10, 'Relegated': 3}
```

All 20 teams passed the arithmetic checks, and the league goals match: 922 scored and 922 conceded.

## Things to know

- `ppg` is 0 for all 20 teams, so calculate points per game yourself.
- Only 10 of 20 teams have a zone label. Zone names say `Relegated` for the last 3.
- I did not get a table for the current 2026-27 season from `Get Standings`, which returned only season details for 2024, 2025 and 2026. Use `/tables` with the last complete season.

## Ideas

- Run the checks every time you refresh the table, and stop if one fails.
- Add a check on the number of teams and games per team for other leagues.
