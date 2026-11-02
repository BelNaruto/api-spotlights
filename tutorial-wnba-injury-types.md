---
image: /assets/wnba-standings-og.jpg
title: Group the WNBA injury report by injury type in Python
description: A short Python script that downloads the WNBA injury report and groups players by injury type, using the WNBA API on RapidAPI.
---

# Group the WNBA injury report by injury type in Python

In this tutorial you will build a script that downloads the WNBA injury report and groups it by type of injury, so you can see at a glance which injuries are most common and which players and teams they affect. It uses the [WNBA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/wnba-api) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [WNBA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/wnba-api) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The injuries endpoint (`/injuries`) needs no parameters. It returns `injuries`, a list with one entry per team. Each entry has the team `displayName` and its own list of `injuries`. Each injury has the player, a `status`, and `details.type` with the injury type (Knee, Foot, Ankle...) and the expected return date.

## 3. The script

Save this as `wnba_injury_types.py`. It retries temporary server errors.

```python
"""WNBA injury report grouped by injury type. Uses the WNBA API on RapidAPI."""
import os, sys, time
from collections import defaultdict
import requests

HOST = "wnba-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def injuries():
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/injuries", headers=HEADERS, timeout=60)
        if r.ok:
            return r.json()["injuries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(top=5):
    by_type = defaultdict(list)
    for team in injuries():
        for item in team["injuries"]:
            by_type[item["details"]["type"]].append((item["athlete"]["displayName"], team["displayName"]))
    total = sum(len(v) for v in by_type.values())
    print(f"{total} players on the WNBA injury report\n")
    for kind, players in sorted(by_type.items(), key=lambda kv: len(kv[1]), reverse=True)[:int(top)]:
        print(f"{kind} ({len(players)})")
        for name, team in players[:3]:
            print(f"  {name.ljust(24)} {team}")


if __name__ == "__main__":
    main(*sys.argv[1:2])
```

## 4. Run it

```bash
python wnba_injury_types.py
```

Real output from the live API:

```
49 players on the WNBA injury report

Knee (18)
  Aicha Coulibaly          Chicago Sky
  Azura Stevens            Chicago Sky
  Natasha Cloud            Chicago Sky
Coach's Decision (8)
  Matilde Villa            Atlanta Dream
  Ndjakalenga Mwenentanda  Los Angeles Sparks
  Shyanne Sellers          Los Angeles Sparks
Leg (3)
  Brionna Jones            Atlanta Dream
  Tyasha Harris            Indiana Fever
  NaLyssa Smith            Las Vegas Aces
Foot (3)
  DiJonai Carrington       Chicago Sky
  Anastasiia Olairi Kosu   Minnesota Lynx
  Brittney Sykes           Toronto Tempo
Ankle (3)
  Saniya Rivers            Connecticut Sun
  Cameron Brink            Los Angeles Sparks
  Aaliyah Nye              Los Angeles Sparks
```

The complete script is in [examples/wnba_injury_types.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/wnba_injury_types.py).

## Tips

- Change `top` to see more injury types.
- Group by team instead of type to see which roster is hit hardest.
- Run it weekly and save the counts to a CSV to track trends.

## Next steps

- [WNBA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/wnba-api) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
