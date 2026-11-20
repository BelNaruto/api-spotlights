---
title: PGA Tour season recap and event leaderboard in Python
image: /assets/golf-event-recap-og.jpg
description: A short Python script that reads the PGA Tour schedule, finds the multiple winners of the season and prints the leaderboard of the latest event, using the Live Golf Data API on RapidAPI.
---

# PGA Tour season recap and event leaderboard in Python

In this tutorial you will build a script that reads the PGA Tour schedule for a season, counts the winners, and prints the full leaderboard of the latest completed event. It uses the [Live Golf Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/live-golf-data1) and about 60 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Live Golf Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/live-golf-data1) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. A small helper to call the API

The helper returns the parsed JSON and retries temporary server errors.

```python
import os, re, sys, time
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

## 3. Read the season schedule

`/schedule` takes a `season` (required) and a `league` (`pga` by default) and returns `events`. Each event has a `name`, `date`, `status` (`pre`, `in` or `post`), `description`, `score`, `winnerAthlete` and a `link` that ends with the tournament id.

One detail matters: scheduled and in-progress events also carry a `winnerAthlete`, which is the defending champion. Only count winners of events with `status == "post"`.

```python
def season_recap(season):
    events = call("/schedule", season=season, league="pga")["events"]
    done = [e for e in events if e["status"] == "post" and not e["isPostponedOrCanceled"]]
    wins = {}
    for e in done:
        name = (e.get("winnerAthlete") or {}).get("name")
        if name:
            wins[name] = wins.get(name, 0) + 1
    multi = sorted(((n, c) for n, c in wins.items() if c > 1), key=lambda kv: (-kv[1], kv[0]))
    print("Multiple winners: " + ", ".join(f"{n} {c}" for n, c in multi))
    return done[-1]
```

## 4. Turn an event into an id

The tournament id is the number at the end of the leaderboard link:

```python
def event_id(event):
    return re.search(r"tournamentId=(\d+)", event["link"]).group(1)
```

## 5. Read the leaderboard

`/leaderboard` takes an `eventId` and returns `events[0]` with the event name, purse, `winner`, `courses` and `competitions[0].competitors`. Each competitor has a `sortOrder` (use it to rank), a `score.displayValue` (score to par), `earnings`, `linescores` for each round and a `status` with the finishing position. Players who missed the cut have the status `STATUS_CUT`.

```python
def leaderboard(event, top=10):
    data = call("/leaderboard", eventId=event_id(event))["events"][0]
    players = sorted(data["competitions"][0]["competitors"], key=lambda c: c["sortOrder"])
    made_cut = [p for p in players if p["status"]["type"]["name"] != "STATUS_CUT"]
    course = data["courses"][0]
    print(f"{data['name']} - {course['name']}, par {course['shotsToPar']}, purse {data['displayPurse']}")
    print(f"Winner: {data['winner']['displayName']} | {len(players)} players, {len(made_cut)} made the cut")
    for p in players[:top]:
        rounds = "-".join(str(int(l["value"])) for l in p["linescores"] if not l.get("isPlayoff") and l.get("value"))
        print(p["status"]["position"]["displayName"], p["athlete"]["displayName"],
              p["score"]["displayValue"], rounds, f"${p['earnings']:,}")
```

Playoff holes show up as an extra entry in `linescores` with `isPlayoff` set to `true`, so the script skips them when it prints the four rounds.

## 6. Run it

```bash
python golf_event_recap.py 2026
```

This is what it printed from live API responses on 2026-11-20:

```
PGA Tour 2026: 49 events on the schedule
  45 completed | 1 in progress | 2 upcoming | 1 canceled
  32 different winners in 43 individual events
Multiple winners: Chris Gotterup 3, Scottie Scheffler 3, Wyndham Clark 3, Austin Smotherman 2, Cameron Young 2, Jacob Bridgeman 2, Matt Fitzpatrick 2, Michael Brennan 2

Latest completed events
  Nov 12-16     Austin Championship pres. by Compliance Solutions   Chad Ramey (268 (-20))
  Nov 5-8       World Wide Technology Championship                  Blades Brown (265 (-23))
  Oct 29-Nov 1  VidantaWorld Mexico Open                            Andrew Novak (259 (-25))

Austin Championship pres. by Compliance Solutions - Omni Barton Creek Resort & Spa (Fazio Canyons Course), par 72, purse $6,000,000
Winner: Chad Ramey | 120 players, 65 made the cut
Pos  Player                To par  Rounds             Money
1    Chad Ramey            -20     68-68-67-65   $1,080,000
2    Ben Kohles            -18     66-69-69-66     $654,000
3    Trace Crowe           -17     62-69-71-69     $414,000
T4   Hayden Springer       -16     70-68-68-66     $252,500
T4   Blades Brown          -16     65-70-71-66     $252,500
T4   Erik van Rooyen       -16     64-70-69-69     $252,500
T7   Jordan Smith          -15     67-67-72-67     $188,500
T7   Austin Smotherman     -15     67-71-67-68     $188,500
T7   Sami Välimäki         -15     68-66-69-70     $188,500
T10  Joel Dahmen           -14     71-69-69-65     $145,500
```

Two of the 45 completed events have no single winner: the Zurich Classic (a team event) and the Presidents Cup, so the script counts 43 individual winners. The leaderboard also shows how the prize money is shared when players tie: the three players tied for 4th each received $252,500.

The complete script is in [examples/golf_event_recap.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/golf_event_recap.py).

## Tips

- Pass `league=lpga`, `liv`, `eur`, `champions-tour` or `ntw` to `/schedule` and `/leaderboard` to cover other tours.
- To follow a tournament live, find the event whose `status` is `in` and poll `/leaderboard` every few minutes. Do not use `winnerAthlete` for events that are not finished.
- The `/leaderboard` response is large (over 200 KB for a full field), so read only what you need and cache it for finished events.

## Next steps

- [Live Golf Data API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/live-golf-data1): all endpoints, plans and live playground.
- Next tutorial: [PGA Tour money list](tutorial-golf-money-list).
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
