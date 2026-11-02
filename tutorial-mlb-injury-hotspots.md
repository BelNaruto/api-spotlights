---
image: /assets/mlb-pythagorean-standings-og.jpg
title: Find MLB injury hotspots by body part and team in Python
description: A short Python script that reads the MLB injury report and shows the most common injuries, the share of pitchers and the teams with most players listed, using the MLB API on RapidAPI.
---

# Find MLB injury hotspots by body part and team in Python

In this tutorial you will build a script that reads the MLB injury report and shows which injuries are most common, how many of the injured players are pitchers, and which teams have the most players listed. It uses the [Major League Baseball (MLB) API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/major-league-baseball-mlb) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Major League Baseball (MLB) API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/major-league-baseball-mlb) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The injuries endpoint (`/injuries`) needs no parameters. It returns `injuries`, one entry per team with a `displayName` and a list of `injuries`. Each injury has `athlete.position.abbreviation`, `status` and `details.type`.

## 3. The script

Save this as `mlb_injury_hotspots.py`. It retries temporary server errors.

```python
import os
import time
from collections import Counter

import requests

HOST = "major-league-baseball-mlb.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}


def injuries():
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/injuries", headers=HEADERS, timeout=60)
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()["injuries"]


def main(top=5):
    teams = injuries()
    by_type, by_team, pitchers, total = Counter(), Counter(), 0, 0
    for team in teams:
        for item in team["injuries"]:
            total += 1
            by_type[item["details"]["type"]] += 1
            by_team[team["displayName"]] += 1
            if item["athlete"]["position"]["abbreviation"] in ("SP", "RP"):
                pitchers += 1
    print(f"{total} players on the MLB injury report across {len(teams)} teams")
    print(f"Pitchers: {pitchers} ({round(100 * pitchers / total)}%)")
    print("\nMost common injuries")
    for kind, n in by_type.most_common(top):
        print(f"  {kind.ljust(12)} {n}")
    print("\nTeams with the most players listed")
    for name, n in by_team.most_common(top):
        print(f"  {name.ljust(24)} {n}")


if __name__ == "__main__":
    main()
```

## 4. Run it

```bash
python mlb_injury_hotspots.py
```

Real output from the live API (the report includes the 60-day IL):

```
186 players on the MLB injury report across 30 teams
Pitchers: 121 (65%)

Most common injuries
  Elbow        80
  Shoulder     26
  Knee         11
  Hip          8
  Wrist        7

Teams with the most players listed
  San Francisco Giants     16
  Boston Red Sox           13
  Seattle Mariners         11
  Athletics                10
  Detroit Tigers           9
```

The complete script is in [examples/mlb_injury_hotspots.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/mlb_injury_hotspots.py).

## Tips

- Filter on `status` to look only at Day-To-Day players.
- Use `details.returnDate` to build a list of players expected back before opening day.
- Add the standings endpoint to compare injuries with results.

## Next steps

- [Major League Baseball (MLB) API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/major-league-baseball-mlb) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
