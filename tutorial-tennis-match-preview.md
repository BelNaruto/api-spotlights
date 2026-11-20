---
title: Build a tennis match preview in Python (head-to-head and win probability)
description: A short Python script that previews any ATP or WTA matchup with head-to-head, Elo, recent form and a win probability, using the Tennis API on RapidAPI.
---

# Build a tennis match preview in Python

In this tutorial you will build a script that takes two player ids and prints a match preview: the head-to-head record by surface, the last meeting, recent form, Elo ratings and a win probability from the model. It uses the [Tennis API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/tennis-api) and about 50 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Tennis API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/tennis-api) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

Every response uses the same envelope: `success`, `message`, `error`, `data` and `meta`. The helper returns `data` and retries temporary upstream errors (502, 503, 504).

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

## 3. Find the player ids

Every player endpoint uses the same id. You can read ids from `/rankings` (each row has `player.id`) or search by name with `/players/search?query=alcaraz`. In this tutorial we use two ids from the current ATP top 3: `3623` (Jannik Sinner) and `3782` (Carlos Alcaraz).

## 4. Head-to-head

`/h2h` takes `player1` and `player2` and returns the overall record in `summary`, a split `bySurface`, the `lastMeeting` and a list of `meetings`.

```python
def head_to_head(p1, p2):
    h = call("/h2h", player1=p1, player2=p2, limit=5)
    s = h["summary"]
    print(f"Head-to-head: {s['player1']}-{s['player2']} in {s['matches']} meetings")
    print("  " + " | ".join(f"{name} {v['player1']}-{v['player2']}" for name, v in s["bySurface"].items()))
    return h
```

## 5. Add the prediction

`/predictions/match` takes the same two ids plus a `surface` (`hard`, `clay` or `grass`) and `bestOf` (3 or 5). It returns win probabilities, the most likely set score and every model component: Elo, ranking points, recent form and head-to-head, each with its weight.

```python
def prediction(p1, p2, surface="hard"):
    return call("/predictions/match", player1=p1, player2=p2, surface=surface, bestOf=3)
```

## 6. Put it together

```python
def preview(p1, p2, surface="hard"):
    h2h = head_to_head(p1, p2)
    pred = prediction(p1, p2, surface)
    a, b = h2h["player1"], h2h["player2"]
    p = pred["prediction"]
    pr = p["probabilities"]
    print(f"Prediction on {pred['surface']} (best of {pred['bestOf']}): "
          f"{a['name']} {pr['player1'] * 100:.1f}% - {b['name']} {pr['player2'] * 100:.1f}% "
          f"(confidence: {p['confidence']})")
    print(f"Most likely score: {p['predictedScore']} | chance of a deciding set: {p['goesTheDistance'] * 100:.1f}%")
```

The full script also prints the last meeting, the Elo ratings and the recent form. Here is what it printed for Sinner vs Alcaraz on hard courts, from live API responses on 2026-11-20:

```
Jannik Sinner (ITA, #2) vs Carlos Alcaraz (ESP, #3)
Head-to-head: 7-11 in 18 meetings
  Clay 2-4 | Hard 3-7 | Grass 2-0
Last meeting: ATP Masters 1000 Monte-Carlo 2026 Final - Jannik Sinner won 7-6(5) 6-3
Prediction on Hard (best of 3): Jannik Sinner 54.7% - Carlos Alcaraz 45.3% (confidence: low)
Most likely score: 2-0 | chance of a deciding set: 49.8%
Elo (hard): 2280 vs 2200
Form, last 10: WWWWWWWLWW vs WWWWWWWWWW
```

Notice how the model reads this matchup: Alcaraz leads the head-to-head 11-7 and has the better recent form, but Sinner has the higher Elo, so the blend ends up slightly in Sinner's favour. The API marks that as `low` confidence because the two probabilities are close.

The complete script is in [examples/tennis_match_preview.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/tennis_match_preview.py). Run it with:

```bash
python tennis_match_preview.py 3623 3782 hard
```

## Tips

- The first request for an endpoint can take several seconds (our first ranking call took about 12 seconds), while repeated identical requests came back in well under a second. Cache results in your own app too and use a generous timeout.
- Use `surface=clay` or `surface=grass` and compare. The surface Elo changes the result.
- Use `bestOf=5` for men's Grand Slam singles.
- The response lists every model component with its weight (`components`), so you can show users why the model picked a player.
- Predictions are statistical estimates, not betting advice.

## Next steps

- [Tennis API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/tennis-api): 43 endpoints, plans and live playground.
- Next tutorial: [Elo ratings vs the ATP ranking](tutorial-tennis-elo-vs-ranking).
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
