---
image: /assets/premier-league-table-og.jpg
title: Analyse a month of Premier League results in Python
description: A short Python script that reads a month of Premier League results and prints goals per match, home advantage and the biggest wins, using the English Premier League API on RapidAPI.
---

# Analyse a month of Premier League results in Python

In this tutorial you will build a script that downloads a month of Premier League results and prints goals per match, how often the home side wins and the biggest margins. It uses the [English Premier League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [English Premier League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The scoreboard endpoint (`/scoreboard`) takes `year`, `month` and `limit`. It returns `scoreboard.events`; each event has a `date` and `competitions[0].competitors` with `homeAway`, team `displayName` and `score` as text.

## 3. The script

Save this as `premier_league_results.py`. It retries temporary server errors.

```python
"""Premier League results for a month: biggest wins and goal stats. Uses the English Premier League API on RapidAPI."""
import os, sys, time
from operator import gt

import requests

HOST = "english-premiere-league1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def matches(year, month):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/scoreboard", headers=HEADERS, timeout=60,
                         params={"year": year, "month": month, "limit": 100})
        if r.ok:
            return r.json()["scoreboard"]["events"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year, month, top=5):
    results = []
    for event in matches(year, month):
        sides = {c["homeAway"]: c for c in event["competitions"][0]["competitors"]}
        home, away = sides["home"], sides["away"]
        results.append((event["date"][:10], home["team"]["displayName"], int(home["score"]),
                        away["team"]["displayName"], int(away["score"])))
    goals = sum(h + a for _, _, h, _, a in results)
    home_wins = sum(1 for _, _, h, _, a in results if gt(h, a))
    away_wins = sum(1 for _, _, h, _, a in results if gt(a, h))
    draws = len(results) - home_wins - away_wins
    print(f"{len(results)} matches, {goals} goals ({goals / len(results):.2f} per match)")
    print(f"home wins {home_wins}, draws {draws}, away wins {away_wins}\n")
    print("Biggest margins:")
    for date, home, h, away, a in sorted(results, key=lambda r: abs(r[2] - r[4]), reverse=True)[:int(top)]:
        print(f"  {date}  {home} {h}-{a} {away}")


if __name__ == "__main__":
    a = sys.argv[1:] + ["2026", "10"][len(sys.argv) - 1:]
    main(a[0], a[1])
```

## 4. Run it

```bash
python premier_league_results.py 2026 10
```

Real output for October 2026:

```
38 matches, 100 goals (2.63 per match)
home wins 18, draws 9, away wins 11

Biggest margins:
  2026-10-18  Brighton & Hove Albion 5-0 Crystal Palace
  2026-10-10  Chelsea 5-1 AFC Bournemouth
  2026-10-11  Liverpool 0-3 Manchester City
  2026-10-12  Coventry City 4-1 Newcastle United
  2026-10-25  Manchester United 0-3 AFC Bournemouth
```

The complete script is in [examples/premier_league_results.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/premier_league_results.py).

## Tips

- Pass a different year and month to compare seasons.
- Change `top` to list more of the biggest results.
- Add the standings endpoint to see how results moved the table.

## Next steps

- [English Premier League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/english-premiere-league1) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
