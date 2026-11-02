---
title: Build a Premier League table with European and relegation zones in Python
description: A short Python script that prints the Premier League table with points per game and qualification and relegation zones, using the English Premier League API on RapidAPI.
---

# Build a Premier League table with European and relegation zones in Python

In this tutorial you will build a script that pulls the Premier League table for any season and prints each club's record, goal difference, points, points per game and the zone it sits in (champion, Champions League, Europa League or relegation). It uses the [English Premier League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1) and about 50 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [English Premier League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Fetch the league table

The tables endpoint (`/tables`) takes a `season` (the starting year, so `2025` is 2025-26) and returns the table in `children[0].standings.entries`, one entry per club. Each entry has the `team` and a `stats` list of named values such as `wins`, `ties`, `losses`, `points`, `pointsFor`, `pointsAgainst`, `pointDifferential` and `gamesPlayed`. The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "english-premiere-league1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def league_table(season):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/tables", headers=HEADERS,
                         params={"season": season}, timeout=60)
        if r.ok:
            return r.json()["children"][0]["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Add the zones and print the table

We sort by points, then goal difference, then goals scored, number the clubs from 1 and label the zones by position. The Europa League spot is simplified to fifth place; real qualification also depends on the cups.

```python
def zone(position, size):
    if position == 1:
        return "CHAMPION"
    if position in (2, 3, 4):
        return "Champions League"
    if position == 5:
        return "Europa League"
    if position in range(size - 2, size + 1):
        return "Relegation"
    return ""


def main(season):
    entries = league_table(season)
    rows = []
    for e in entries:
        s = {x["name"]: x.get("value") for x in e["stats"]}
        rows.append((s["points"], s["pointDifferential"], s["pointsFor"], e["team"]["displayName"], s))
    rows.sort(reverse=True)
    print("#".rjust(2) + "  " + "Team".ljust(24) + "P".rjust(3) + "  W-D-L".ljust(10) + "GD".rjust(4) + "PTS".rjust(5) + "  PPG   Zone")
    for pos, (pts, gd, gf, team, s) in enumerate(rows, 1):
        record = f"{s['wins']:.0f}-{s['ties']:.0f}-{s['losses']:.0f}"
        ppg = pts / s["gamesPlayed"]
        print(f"{pos:2}  " + team.ljust(24) + f"{s['gamesPlayed']:3.0f}  " + record.ljust(8) +
              f"{gd:+4.0f}{pts:5.0f}  {ppg:.2f}  {zone(pos, len(rows))}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["2025"])[0])
```

## 4. Run it

```bash
python premier_league_table.py 2025
```

You get the full 20-club table (illustrative layout):

```
 #  Team                      P  W-D-L     GD  PTS  PPG   Zone
 1  Arsenal                  38  26-7-5   +44   85  2.24  CHAMPION
 2  Man City                 38  25-8-5   +35   83  2.18  Champions League
```

The complete script is in [examples/premier_league_table.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/premier_league_table.py).

## Tips

- Run it during the season and the games played column shows who has games in hand.
- Points per game is the fairest way to compare clubs that have played a different number of matches.
- The API also has fixtures, box scores, team rosters, player statistics, transfers and news you can add next.

## Next steps

- [English Premier League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
