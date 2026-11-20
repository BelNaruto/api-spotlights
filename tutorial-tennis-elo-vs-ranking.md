---
title: Elo ratings vs the ATP ranking in Python (who is really playing best?)
description: A short Python script that compares the official ATP ranking with surface Elo ratings and lists the biggest ranking movers, using the Tennis API on RapidAPI.
---

# Elo ratings vs the ATP ranking in Python

The ATP ranking rewards points collected over 52 weeks. An Elo rating reacts to who you actually beat, and on which surface. In this tutorial you will build a script that puts the two side by side for any surface and lists the biggest risers and fallers of the latest ranking week. It uses the [Tennis API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/tennis-api) and about 40 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Tennis API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/tennis-api) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

The helper returns the `data` part of the response envelope and retries temporary upstream errors.

```python
import os, sys, time
import requests

HOST = "tennis-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}

def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Get the Elo leaderboard

`/predictions/ratings` returns the Elo ratings used by the prediction model. Pass a `surface` (`hard`, `clay` or `grass`) to get the rating blended with that surface, and `limit` for the number of players. Each row has `rank`, `id`, `name` and `rating`.

```python
elo = call("/predictions/ratings", surface="hard", limit=10)["ratings"]
```

## 4. Get the official ranking

`/rankings` returns the ATP singles ranking with `rank` and `points` for each `player`. Ask for the top 100 and index it by player id, so we can look up any Elo player.

```python
atp = {r["player"]["id"]: r for r in call("/rankings", limit=100)["rankings"]}
```

## 5. Print the comparison

Both lists use the same player ids, so the join is one dictionary lookup. Players outside the top 100 are shown as `>100`.

```python
print(f"{'Elo#':<5}{'Player':<30}{'Elo':>5}  {'ATP#':>5}{'Points':>8}")
for e in elo:
    r = atp.get(e["id"])
    rank = f"{r['rank']}" if r else ">100"
    points = f"{r['points']}" if r else "-"
    print(f"{e['rank']:<5}{e['name']:<30}{e['rating']:>5}  {rank:>5}{points:>8}")
```

## 6. Add the ranking movers

`/rankings/movers` returns `risers` and `fallers` for the latest ranking week. `top=100` limits it to players inside the top 100.

```python
movers = call("/rankings/movers", limit=3, top=100)
for m in movers["risers"]:
    print(f"  +{m['movement']}  #{m['rank']}  {m['player']['name']} ({m['player']['countryCode']})")
```

## 7. Run it

```bash
python tennis_elo_vs_ranking.py hard
```

This is what it printed from live API responses on 2026-11-20 (ranking week of 2026-11-16):

```
Top 10 by Elo on hard courts vs the official ATP ranking
Elo# Player                          Elo   ATP#  Points
1    Jannik Sinner                  2280      2    7950
2    Carlos Alcaraz                 2200      3    6100
3    Alexander Zverev               2029      1    9350
4    Ben Shelton                    1963      4    5170
5    Taylor Fritz                   1938      9    3300
6    Novak Djokovic                 1936     12    2940
7    Daniil Medvedev                1931      5    3820
8    Alejandro Davidovich Fokina    1909     16    2500
9    Arthur Fils                    1898      7    3625
10   Alex de Minaur                 1894     11    3170

Biggest risers in the latest ranking week
  +7  #100  Aleksandr Shevchenko (KAZ)
  +4  #47  Thiago Agustin Tirante (ARG)
  +3  #92  Toby Samuel (GBR)
Biggest fallers
  -3  #17  Felix Auger-Aliassime (CAN)
  -2  #11  Alex de Minaur (AUS)
  -2  #27  Lorenzo Musetti (ITA)
```

The table shows why Elo is useful: the official number 1, Alexander Zverev, is third on hard-court Elo, while Sinner (ATP #2) and Alcaraz (ATP #3) sit on top. Novak Djokovic is only 12th in the ranking but 6th in Elo. Gaps like these are a quick way to spot players who are better, or worse, than their ranking says.

The complete script is in [examples/tennis_elo_vs_ranking.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/tennis_elo_vs_ranking.py).

## Tips

- Try `python tennis_elo_vs_ranking.py clay` and compare the table: surface Elo moves players a lot.
- Add `tour=wta` to both calls to build the same table for the women's tour.
- `/rankings?kind=race` returns the ATP Race to Turin if you want the current-season view.
- Elo and ranking are refreshed regularly, so cache them for a few hours instead of calling on every page view.

## Next steps

- [Tennis API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/tennis-api): 43 endpoints, plans and live playground.
- Previous tutorial: [Tennis match preview](tutorial-tennis-match-preview).
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
