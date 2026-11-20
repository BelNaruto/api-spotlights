---
title: Build a PGA Tour money list in Python (earnings, FedExCup points, wins)
description: A short Python script that prints the PGA Tour money list with earnings, FedExCup points, wins and driving distance, using the Live Golf Data API on RapidAPI.
---

# Build a PGA Tour money list in Python

In this tutorial you will build a script that prints the PGA Tour money list for a season: official earnings, FedExCup points, events played, top 10 finishes, wins, driving distance and greens in regulation. It uses the [Live Golf Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/live-golf-data1) and about 40 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Live Golf Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/live-golf-data1) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

```python
import os, sys, time
import requests

HOST = "live-golf-data1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}

def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Call the player stats endpoint

`/players-stats` takes `league` (`pga` by default), `season` (it defaults to 2024, so always pass the season you want), `page` and `limit`. The players come back ordered by official earnings, and each one has `athlete` (with `displayName`) and `categories[0].totals`, a list of stat values as text.

```python
athletes = call("/players-stats", league="pga", season="2026", limit=10)["players_stats"]["athletes"]
```

## 4. Read the stats by position

The response also contains a `glossary` that describes each stat, but it is sorted alphabetically and does not follow the order of `totals`. So read the numbers by position. This is the mapping we use (we checked it against the 2026 schedule: the win counts match the number of events each player won):

```python
EARNINGS, FEDEX_POINTS, EVENTS, CUTS_MADE, TOP10, WINS, GREENS_PCT, DRIVE_YDS = 0, 1, 2, 4, 5, 6, 7, 8
```

## 5. Print the table

```python
for i, a in enumerate(athletes, 1):
    t = a["categories"][0]["totals"]
    print(f"{i:<3}{a['athlete']['displayName']:<20}{t[EARNINGS]:>12}{t[FEDEX_POINTS]:>10}{t[EVENTS]:>7}"
          f"{t[CUTS_MADE]:>6}{t[TOP10]:>6}{t[WINS]:>5}{t[DRIVE_YDS]:>7}{t[GREENS_PCT]:>6}")
```

Then add one more line, using the driving distance to find the longest hitter in the list:

```python
best = max(athletes, key=lambda a: float(a["categories"][0]["totals"][DRIVE_YDS]))
print(f"Longest driver in this top 10: {best['athlete']['displayName']} ({best['categories'][0]['totals'][DRIVE_YDS]} yards)")
```

## 6. Run it

```bash
python golf_money_list.py 2026
```

This is what it printed from live API responses on 2026-11-20:

```
PGA Tour 2026 money list (top 10)
#  Player                  Earnings FedEx pts Events  Cuts Top10 Wins  Drive  GIR%
1  Scottie Scheffler    $30,937,524      4986     20    19    13    3  312.7  67.9
2  Cameron Young        $15,068,482      3206     20    20     8    2  318.3  69.2
3  Matt Fitzpatrick     $14,679,817      3463     21    19     8    3  306.3  69.0
4  Wyndham Clark        $14,661,436      3292     25    18     6    3  313.2  69.2
5  Jacob Bridgeman      $11,589,508      1961     25    24     8    2  305.9  69.0
6  Rory McIlroy         $11,573,749      2095     14    13     6    1  330.3  69.2
7  Viktor Hovland       $11,495,826      1425     19    15     4    1  306.1  69.5
8  Ryan Gerard          $10,475,998      1608     28    23     9    0  308.2  69.1
9  Chris Gotterup       $10,446,028      2588     23    21     7    3  322.9  69.1
10 Si Woo Kim           $10,271,694      2729     24    23    11    0  302.2  69.0

Longest driver in this top 10: Rory McIlroy (330.3 yards)
```

A few things stand out. Scottie Scheffler has more than double the earnings of anyone else, and the FedExCup points show a different order than money: Matt Fitzpatrick has more points than Cameron Young but earned less. Rory McIlroy leads the group in driving distance while playing only 14 events.

The complete script is in [examples/golf_money_list.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/golf_money_list.py).

## Tips

- Use `page` and `limit` to walk through the whole field (the default `limit` is 50).
- `league` accepts the other tours too (`lpga`, `liv`, `eur`, `champions-tour`, `ntw`).
- Totals change after every tournament, so cache the table for a few hours.

## Next steps

- [Live Golf Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/live-golf-data1): all endpoints, plans and live playground.
- Previous tutorial: [PGA Tour season recap and event leaderboard](tutorial-golf-event-recap).
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
