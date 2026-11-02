---
title: Build an F1 championship table with points gaps in Python
description: A short Python script that prints the Formula 1 drivers championship with the gap to the leader and each driver's best race, using the F1 Motorsport Data API on RapidAPI.
image: /assets/f1-standings-og.jpg
---

# Build an F1 championship table with points gaps in Python

In this tutorial you will build a script that prints the Formula 1 drivers championship for any season, with the points gap to the leader and each driver's best race haul. It uses the [F1 Motorsport Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/f1-motorsport-data) and about 35 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [F1 Motorsport Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/f1-motorsport-data) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Get the standings

`/standings-drivers` takes a `year` and returns `standings.entries`, one per driver. Each entry has an `athlete` (with `displayName`) and a `stats` list. Two stats are named `rank` and `championshipPts`. The other stats are one per race: they have `played`, the race `shortName` and the points `value` scored in that race.

```python
import os, sys, time
import requests

HOST = "f1-motorsport-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def driver_standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/standings-drivers", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Build the table

Turn the stats list into a lookup by name, find each driver's best race and print the gap to the leader.

```python
def main(year="2024", top=10):
    rows = []
    for e in driver_standings(year):
        stats = {s["name"]: s for s in e["stats"]}
        races = [s for s in e["stats"] if s.get("played")]
        best = max(races, key=lambda s: s["value"]) if races else None
        rows.append((stats["rank"]["value"], e["athlete"]["displayName"],
                     stats["championshipPts"]["value"], len(races), best))
    rows.sort()
    leader = rows[0][2]
    print(f"F1 {year} drivers championship")
    for rank, name, pts, n, best in rows[:int(top)]:
        gap = "leader" if pts == leader else f"-{leader - pts:g}"
        peak = f"best: {best['value']:g} pts at {best['shortName']}" if best else ""
        print(f"{int(rank):2d}. {name.ljust(20)} {pts:6g} pts  {gap.rjust(7)}  {peak}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
```

## 4. Run it

```bash
python f1_standings.py 2024 10
```

The first argument is the season and the second is how many drivers to show. Output looks like (illustrative):

```
F1 2024 drivers championship
 1. Driver One             437 pts   leader  best: 26 pts at Race A GP
 2. Driver Two             300 pts     -137  best: 25 pts at Race B GP
```

The complete script is in [examples/f1_standings.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/f1_standings.py).

## Tips

- Loop over several years to build an all-time table.
- The API also has constructor standings, schedule, race results, driver stats and news endpoints.
- Run it after every race weekend and post the table to a Discord or Telegram channel.

## Next steps

- [F1 Motorsport Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/f1-motorsport-data): all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
