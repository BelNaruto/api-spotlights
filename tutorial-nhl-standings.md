---
title: Build an NHL standings table in Python
description: A short Python script that prints the NHL standings with points percentage and goal differential, using the NHL API on RapidAPI.
image: /assets/nhl-standings-og.jpg
---

# Build an NHL standings table in Python

In this tutorial you will build a script that pulls the NHL standings for any season and prints a ranked table with games played, record, points, points percentage and goal differential. It uses the [NHL API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/nhl-api5) and about 35 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [NHL API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/nhl-api5) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Fetch the standings

The NHL Standings endpoint (`/nhlstandings`) takes a `year` (the season's ending year, so `2025` is 2024-25) and returns `standings.entries`, one entry per team. Each entry has the `team` and a `stats` list of named values such as `points`, `wins`, `losses`, `otLosses` and `gamesPlayed`. The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "nhl-api5.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/nhlstandings", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Rank the teams

Points alone are misleading when teams have played different numbers of games, so we sort by points percentage (points divided by the 2 points available per game). We turn each `stats` list into a dictionary first so we can read values by name.

```python
def main(year, top):
    rows = []
    for e in standings(year):
        s = {x["name"]: x.get("value") for x in e["stats"]}
        gp, pts = s["gamesPlayed"], s["points"]
        rows.append((pts / (2 * gp), e["team"]["displayName"], gp, s["wins"], s["losses"],
                     s["otLosses"], pts, s["pointDifferential"]))
    rows.sort(reverse=True)
    print(" #.  " + "Team".ljust(22) + " GP  " + "W-L-OTL".ljust(8) + " PTS  PTS%   GD")
    for i, (pct, team, gp, w, l, otl, pts, gd) in enumerate(rows[:top], 1):
        record = f"{w:.0f}-{l:.0f}-{otl:.0f}"
        print(f"{i:2}.  " + team.ljust(22) + f" {gp:2.0f}  " + record.ljust(8) + f"{pts:4.0f}  {pct:5.3f}  {gd:+.0f}")


if __name__ == "__main__":
    args = sys.argv[1:] + ["2025", "10"][len(sys.argv) - 1:]
    main(args[0], int(args[1]))
```

## 4. Run it

```bash
python nhl_standings.py 2025 5
```

You get the top teams of that season (illustrative layout):

```
 #.  Team                   GP  W-L-OTL  PTS  PTS%   GD
 1.  Winnipeg Jets          82  56-22-4  116  0.707  +86
 2.  Washington Capitals    82  51-22-9  111  0.677  +57
```

The complete script is in [examples/nhl_standings.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/nhl_standings.py).

## Tips

- Run it during the season: teams have played different numbers of games, which is exactly why points percentage is the fairer ranking.
- The endpoint also takes an optional `group` (`league`, `conference` or `division`) if you want grouped tables.
- The API also has scoreboards, box scores, team rosters, injuries, news and picks you can add next.

## Next steps

- [NHL API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/nhl-api5): all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
