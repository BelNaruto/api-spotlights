---
title: Build a Premier League team scoring leaderboard with Python
image: /assets/premier-league-scoring-leaders-og.jpg
description: A Python script that prints a team's top scorers, assist makers and shooters plus season totals, using the English Premiere League API on RapidAPI.
---

# Build a Premier League scoring leaderboard with Python

One call returns goal, assist, shot, pass, foul and save leaders for a team. The script prints the top three in each category and adds up the totals. It uses the [English Premiere League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /team/statistic/scoring` with `teamId` and `season`. The response has `results.stats`, a list of 12 categories: `goalsLeaders`, `assistsLeaders`, `goals`, `assists`, `shotsOnTarget`, `yellowCards`, `redCards`, `foulsCommitted`, `foulsSuffered`, `totalShots`, `accuratePasses` and `saves`. Each has a `leaders` list with `athlete.displayName`, `value` and `displayValue`. Full script: [`examples/premier_league_scoring_leaders.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/premier_league_scoring_leaders.py).

```python
body = call("/team/statistic/scoring", teamId="364", season="2025")
stats = {s["name"]: s["leaders"] for s in body["results"]["stats"]}
print(stats["goals"][0]["athlete"]["displayName"], stats["goals"][0]["value"])
```

```bash
python premier_league_scoring_leaders.py 364 2025
```

## Real output (20 Nov 2026)

Liverpool, 2025-26:

| Category | Top three |
|----------|-----------|
| Goals | Hugo Ekitike 11, Cody Gakpo 7, Mohamed Salah 7 |
| Assists | Dominik Szoboszlai 7, Mohamed Salah 7, Cody Gakpo 5 |
| Shots on target | Szoboszlai 23, Gakpo 21, Ekitike 19 |
| Total shots | Gakpo 87, Szoboszlai 71, Salah 68 |
| Saves | Alisson Becker 57, Giorgi Mamardashvili 34, Freddie Woodman 8 |

Adding up the 24 players listed gives 61 goals, 44 assists, 175 shots on target, 589 shots, 17,301 accurate passes and 99 saves. 9 of the 24 players had no goal.

## Things to know

- The response is large, about 1.1 MB and 2.5 seconds in this run, because every category lists every player. Cache it.
- The `goalsLeaders` and `assistsLeaders` entries add the match count to `displayValue` ("Matches: 28, Goals: 11"), while `goals` and `assists` only hold the number.
- Goalkeepers have their own `saves` category, so use it for them and the other categories for outfield players.
- The `season` default in the playground is 2023.

## Ideas

- Compare goals per match across several teams.
- Turn the leaders into a card for a fan site, refreshed once a day.
