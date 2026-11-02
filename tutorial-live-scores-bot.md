---
title: Build a live sports scores alert bot in Python
description: A short Python bot that polls today's NBA, NFL and MLB games and alerts you on live score changes and final results, using the Sports Information API on RapidAPI.
image: /assets/sports-information-api-og.jpg
---

![Live scores bot](assets/sports-information-api.png)

# Build a live sports scores alert bot in Python

In this tutorial you will build a bot that checks today's games every minute and prints an alert when a score changes or a game ends. You can also send the alerts to Telegram. It uses the [Sports Information API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sports-information) and about 55 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Sports Information API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sports-information) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Fetch today's games

`/today` takes `leagues` (a comma separated list such as `nba,nfl,mlb`) and an optional `date`. Every response has `success`, `data` and `error`. Under `data` you get one item per league with its `name` and an `events` list.

```python
import os, sys, time
import requests

HOST = "sports-information.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def today(leagues):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/today", headers=HEADERS,
                         params={"leagues": leagues}, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Send alerts

Alerts are printed. If you set `TELEGRAM_TOKEN` (from @BotFather) and `TELEGRAM_CHAT_ID`, they are also sent to that Telegram chat.

```python
def notify(text):
    print(text, flush=True)
    token, chat = os.environ.get("TELEGRAM_TOKEN"), os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      data={"chat_id": chat, "text": text}, timeout=30)
```

## 4. Format a score line

Each event has `away` and `home` objects with a `score` and a `team` (with `abbreviation`, `displayName`, logo and records). `status.state` is `pre`, `in` or `post`, and `status.shortDetail` is a readable clock such as `Q2 5:00`.

```python
def line(ev):
    away, home = ev["away"], ev["home"]
    return f"{away['team']['abbreviation']} {away['score']} - {home['score']} {home['team']['abbreviation']}"
```

## 5. Poll and compare

Remember the last state and score of every game. When they change, send an alert: `LIVE` for score changes while a game is in progress, `FINAL` when it ends. Games that have not started are only stored as a baseline.

```python
def main(leagues="nba,nfl,mlb", every=60):
    seen = {}  # event id to (state, score text)
    while True:
        for lg in today(leagues):
            for ev in lg["events"]:
                state, score = ev["status"]["state"], line(ev)
                old = seen.get(ev["id"])
                if old is None and state == "pre":
                    pass  # baseline only
                elif old != (state, score):
                    if state == "in":
                        notify(f"LIVE {lg['name']}: {score}  ({ev['status']['shortDetail']})")
                    elif state == "post":
                        notify(f"FINAL {lg['name']}: {score}")
                seen[ev["id"]] = (state, score)
        time.sleep(every)


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "nba,nfl,mlb")
```

## 6. Run it

```bash
python live_scores_bot.py nba,nfl,mlb
```

While games are on you will see lines like (illustrative numbers):

```
LIVE NBA: OKC 10 - 8 CLE  (Q2 5:00)
FINAL NBA: OKC 100 - 99 CLE
```

The complete script is in [examples/live_scores_bot.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/live_scores_bot.py).

## Tips

- Keep the interval at 30 to 60 seconds. Each poll is one request for all leagues.
- Pass one league, for example `nba`, to keep responses small.
- The API also has game predictions and per league scoreboards you can add to the alerts.

## Next steps

- [Sports Information API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sports-information): all endpoints, plans and live playground.
- [API guide](sports-information-api): features and use cases.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
