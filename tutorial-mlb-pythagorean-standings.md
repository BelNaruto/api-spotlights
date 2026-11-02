---
image: /assets/mlb-pythagorean-standings-og.jpg
title: Find lucky and unlucky MLB teams with Pythagorean standings in Python
description: A short Python script that compares MLB win totals with the wins their runs scored and allowed predict, using the MLB API on RapidAPI.
---

# Find lucky and unlucky MLB teams with Pythagorean standings in Python

In this tutorial you will build a script that pulls the MLB standings for a season and compares each team's actual wins with the wins its runs scored and runs allowed predict (the Pythagorean expectation). Teams far above the expected line were lucky, teams far below were unlucky. It uses the [MLB API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/major-league-baseball-mlb) and about 45 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [MLB API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/major-league-baseball-mlb) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Fetch the standings

The `/standings` endpoint takes a `year` and returns `standings.entries`, one per team. Each entry has the `team` and a `stats` list of named values. We need `wins`, `losses`, `winPercent`, `pointsFor` (runs scored) and `pointsAgainst` (runs allowed). The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "major-league-baseball-mlb.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/standings", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Compute the Pythagorean expectation

The expected win percentage is runs scored to the power 1.83, divided by the sum of runs scored and runs allowed each to the power 1.83. Multiply by games played to get expected wins, then compare with real wins.

```python
def pythagorean(runs_scored, runs_allowed):
    """Expected win percentage from runs scored and allowed (exponent 1.83)."""
    rs, ra = runs_scored ** 1.83, runs_allowed ** 1.83
    return rs / (rs + ra)


def main(year):
    rows = []
    for e in standings(year):
        s = {x["name"]: x.get("value") for x in e["stats"]}
        games = s["wins"] + s["losses"]
        expected = pythagorean(s["pointsFor"], s["pointsAgainst"]) * games
        rows.append((s["winPercent"], e["team"]["displayName"], s["wins"], s["losses"],
                     s["pointsFor"], s["pointsAgainst"], s["wins"] - expected))
    rows.sort(reverse=True)
    print("Team".ljust(24) + "W-L".ljust(9) + "RS".ljust(6) + "RA".ljust(6) + "RUN DIFF".ljust(10) + "WINS VS EXPECTED")
    for pct, team, w, l, rs, ra, luck in rows:
        print(team.ljust(24) + f"{w:.0f}-{l:.0f}".ljust(9) + f"{rs:.0f}".ljust(6) +
              f"{ra:.0f}".ljust(6) + f"{rs - ra:+.0f}".ljust(10) + f"{luck:+.1f}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["2025"])[0])
```

## 4. Run it

```bash
python mlb_pythagorean.py 2025
```

You get one line per team, best record first (illustrative numbers):

```
Team                    W-L      RS    RA    RUN DIFF  WINS VS EXPECTED
New York Yankees        94-68    849   685   +164      -2.7
Chicago Cubs            92-70    780   690   +90       +2.0
```

The complete script is in [examples/mlb_pythagorean.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/mlb_pythagorean.py).

## Tips

- A positive last column means the team won more games than its run totals suggest. Those teams often regress the next season.
- The endpoint also takes an optional `group` parameter if you want a different grouping.
- The API also has scoreboards, box scores, play by play, schedules, injuries, team rosters and news you can add next.

## Next steps

- [MLB API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/major-league-baseball-mlb) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
