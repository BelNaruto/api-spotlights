---
image: /assets/nba-injury-report-og.jpg
title: Print NBA game results with quarter scores in Python
description: A short Python script that prints every NBA game on a date with the winner and quarter-by-quarter scores, using the Basketball API on RapidAPI.
---

# Print NBA game results with quarter scores in Python

In this tutorial you will build a script that prints every NBA game on a given date, home team first, with the winner marked and the points scored in each quarter. It uses the [Basketball API (NBA)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/api-basketball-nba) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Basketball API (NBA)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/api-basketball-nba) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The scoreboard endpoint (`/nbascoreboard`) takes `year`, `month` and `day`. It returns `events`, and each event has a `shortName`, a `shortDetail` such as Final, and two `competitors` with `homeAway`, `winner`, `score` and a `linescores` list with the points per period.

## 3. The script

Save this as `nba_game_results.py`. It retries temporary server errors.

```python
"""NBA game results with quarter scores. Uses the Basketball API (NBA) on RapidAPI."""
import os, sys, time
import requests

HOST = "api-basketball-nba.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def scoreboard(year, month, day):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/nbascoreboard", headers=HEADERS, timeout=60,
                         params={"year": year, "month": month, "day": day, "limit": 20})
        if r.ok:
            return r.json()["events"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year, month, day):
    games = scoreboard(year, month, day)
    print(f"{len(games)} games on {year}-{month}-{day}\n")
    for game in games:
        comp = game["competitions"][0]["competitors"]
        print(f"{game['shortName']}  ({game['status']['type']['shortDetail']})")
        for team in sorted(comp, key=lambda c: c["homeAway"], reverse=True):
            quarters = "  ".join(q["displayValue"].rjust(2) for q in team["linescores"])
            mark = "W" if team["winner"] else " "
            print(f"  {mark} {team['team']['displayName'].ljust(24)} {quarters}  = {team['score'].rjust(3)}")


if __name__ == "__main__":
    main(*(sys.argv[1:] + ["2026", "11", "01"][len(sys.argv) - 1:]))
```

## 4. Run it

```bash
python nba_game_results.py 2026 11 01
```

Real output for 1 November 2026:

```
4 games on 2026-11-01

BOS @ ORL  (Final)
    Orlando Magic            23  27  24  23  =  97
  W Boston Celtics           24  31  22  31  = 108
BKN @ IND  (Final)
    Indiana Pacers           19  21  22  28  =  90
  W Brooklyn Nets            20  23  28  27  =  98
LAC @ GS  (Final)
  W Golden State Warriors    29  34  29  32  = 124
    LA Clippers              37  20  28  27  = 112
TOR @ LAL  (Final)
  W Los Angeles Lakers       36  30  38  27  = 131
    Toronto Raptors          23  31  28  43  = 125
```

The complete script is in [examples/nba_game_results.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/nba_game_results.py).

## Tips

- Pass yesterday's date from cron to post results to Telegram or Slack every morning.
- Compare `linescores` to find games decided in the fourth quarter.
- Add the box score and play by play endpoints for player lines.

## Next steps

- [Basketball API (NBA)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/api-basketball-nba) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
