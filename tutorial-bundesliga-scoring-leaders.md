---
title: Find a Bundesliga team's top scorers, assisters and shooters with Python
image: /assets/bundesliga-scoring-leaders-og.jpg
description: A Python script that prints a Bundesliga team's goal, assist, shot and save leaders with season totals, using the German Bundesliga API on RapidAPI.
---

# Find a Bundesliga team's scoring leaders with Python

One call returns goal, assist, shot, pass, foul and save leaders for a team. The script prints the top three in five categories and the totals. It uses the [German Bundesliga API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/german-bundesliga-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /team/statistic/scoring` with `teamId` and `season` (`2025` is 2025-26). The response has `team`, `requestedSeason` and `results.stats`, a list of 12 categories (`goalsLeaders`, `assistsLeaders`, `goals`, `assists`, `shotsOnTarget`, `yellowCards`, `redCards`, `foulsCommitted`, `foulsSuffered`, `totalShots`, `accuratePasses`, `saves`). Each has `leaders` with `athlete.displayName` and `value`. Get team ids from the Team List endpoint. Full script: [`examples/bundesliga_scoring_leaders.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/bundesliga_scoring_leaders.py).

```python
body = call("/team/statistic/scoring", teamId="131", season="2025")
stats = {s["name"]: s["leaders"] for s in body["results"]["stats"]}
print(stats["goals"][0]["athlete"]["displayName"], stats["goals"][0]["value"])
```

```bash
python bundesliga_scoring_leaders.py 131 2025
```

## Real output (20 Nov 2026)

Team `131` is Bayer Leverkusen, season 2025-26:

| Category | Top three |
|----------|-----------|
| Goals | Patrik Schick 16, Alejandro Grimaldo 8, Malik Tillman 6 |
| Assists | Aleix García 8, Alejandro Grimaldo 8, Ernest Poku 5 |
| Shots on target | Schick 34, Grimaldo 21, Christian Kofane 19 |
| Total shots | Schick 72, Grimaldo 60, Ibrahim Maza 54 |
| Saves | Mark Flekken 79, Janis Blaswich 39, Aleix García 0 |

The 24 players listed add up to 67 goals, 49 assists, 176 shots on target, 513 shots and 118 saves. 8 of the 24 had no goal.

## Things to know

- The player goals add up to 67 while the Bundesliga table gives Leverkusen 68 goals for. The two sources do not match by one, so use the table for the team total.
- The `saves` list includes outfield players with 0, such as Aleix García, so filter for values above zero.
- The `season` default in the playground is 2023.
- Keep the retry logic in `call()`, the response is large and a call can fail now and then.

## Ideas

- Run it for all 18 teams and rank the league's top scorers.
- Compare Schick's shots and goals to build a shot conversion rate.
