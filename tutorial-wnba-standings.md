---
image: /assets/wnba-standings-og.jpg
title: Build a WNBA standings table with scoring margins in Python
description: A short Python script that ranks WNBA teams by win percentage and shows points for, points against and scoring margin, using the WNBA API on RapidAPI.
---

# Build a WNBA standings table with scoring margins in Python

In this tutorial you will build a script that pulls the WNBA standings for any season and prints every team ranked by win percentage, with average points scored, average points allowed and the scoring margin. It uses the [WNBA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/wnba-api) and about 35 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [WNBA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/wnba-api) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Fetch the standings

The WNBA Standings endpoint (`/wnbastandings`) takes a `year` (the season, for example `2025`) and returns `standings.entries`, one entry per team. Each entry has the `team` and a `stats` list of named values such as `wins`, `losses`, `winPercent`, `avgPointsFor` and `avgPointsAgainst`. The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "wnba-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/wnbastandings", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Rank the teams

We turn each `stats` list into a dictionary so values can be read by name, then sort by win percentage and print the average scoring margin (points for minus points against).

```python
def main(year):
    rows = []
    for e in standings(year):
        s = {x["name"]: x.get("value") for x in e["stats"]}
        margin = s["avgPointsFor"] - s["avgPointsAgainst"]
        rows.append((s["winPercent"], e["team"]["displayName"], s["wins"], s["losses"],
                     s["avgPointsFor"], s["avgPointsAgainst"], margin))
    rows.sort(reverse=True)
    print("Team".ljust(24) + "W-L".ljust(8) + "WIN%".ljust(7) + "PF".ljust(7) + "PA".ljust(7) + "MARGIN")
    for pct, team, w, l, pf, pa, margin in rows:
        record = f"{w:.0f}-{l:.0f}"
        print(team.ljust(24) + record.ljust(8) + f"{pct:.3f}".ljust(7) +
              f"{pf:.1f}".ljust(7) + f"{pa:.1f}".ljust(7) + f"{margin:+.1f}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["2025"])[0])
```

## 4. Run it

```bash
python wnba_standings.py 2025
```

You get one line per team, best record first (illustrative numbers):

```
Team                    W-L     WIN%   PF     PA     MARGIN
Minnesota Lynx          34-10   0.773  86.1   76.7   +9.4
Las Vegas Aces          30-14   0.680  84.0   79.5   +4.5
```

The complete script is in [examples/wnba_standings.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/wnba_standings.py).

## Tips

- Scoring margin is often a better predictor of future results than the win-loss record, so look for teams whose margin is much better than their record.
- The endpoint also takes an optional `group` (`league` or `conference`) if you want grouped tables.
- The API also has scoreboards, box scores, play by play, team rosters, player stats and news you can add next.

## Next steps

- [WNBA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/wnba-api) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
