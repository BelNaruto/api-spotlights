---
image: /assets/nba-injury-report-og.jpg
title: Build an NBA injury report by team in Python
description: A short Python script that prints the current NBA injury report grouped by team, with player, position, status and expected return date, using the Basketball API on RapidAPI.
---

# Build an NBA injury report by team in Python

In this tutorial you will build a script that downloads the current NBA injury report and prints it team by team, with each player's position, status and expected return date. You can filter by team name. It uses the [Basketball API (NBA)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/api-basketball-nba) and about 40 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Basketball API (NBA)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/api-basketball-nba) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Download the injury report

The injuries endpoint (`/nba-injuries`) needs no parameters. It returns `injuries`, one entry per team with a `displayName` and a list of `injuries`. Each injury has the `athlete` (name and position), a `status` such as `Out` or `Day-To-Day`, a `shortComment` and `details.returnDate` when known. The helper retries temporary server errors.

```python
import os, sys, time
import requests

HOST = "api-basketball-nba.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def injuries():
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/nba-injuries", headers=HEADERS, timeout=60)
        if r.ok:
            return r.json()["injuries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Print it by team

Teams are sorted by how many players they have on the report. Pass team names on the command line to see only those teams.

```python
def main(teams):
    data = injuries()
    data.sort(key=lambda t: len(t["injuries"]), reverse=True)
    total = sum(len(t["injuries"]) for t in data)
    print(f"{total} players on the injury report across {len(data)} teams\n")
    for team in data:
        name = team["displayName"]
        if teams and not any(t.lower() in name.lower() for t in teams):
            continue
        if not team["injuries"]:
            continue
        print(f"{name} ({len(team['injuries'])})")
        for item in team["injuries"]:
            player = item["athlete"]
            back = item.get("details", {}).get("returnDate", "unknown")
            print(f"  {player['displayName'].ljust(24)} {player['position']['abbreviation'].ljust(3)} "
                  f"{item['status'].ljust(12)} back: {back}")


if __name__ == "__main__":
    main(sys.argv[1:])
```

## 4. Run it

```bash
python nba_injury_report.py lakers celtics
```

You get the report team by team (an excerpt of the real output):

```
101 players on the injury report across 29 teams

Atlanta Hawks (5)
  Kingston Flemings        G   Suspension   back: 2026-11-04
  Jalen Johnson            F   Day-To-Day   back: 2026-11-02
```

The complete script is in [examples/nba_injury_report.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/nba_injury_report.py).

## Tips

- Run it every morning and send the output to Telegram or Slack before games start.
- The `shortComment` field has a one-line news note you can print next to each player.
- The API also has the scoreboard, game summaries, box scores, play by play, pick center odds, team schedules and news you can add next.

## Next steps

- [Basketball API (NBA)](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/api-basketball-nba) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
