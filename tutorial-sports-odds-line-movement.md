---
title: Track NFL betting line movement with Python
image: /assets/sports-odds-line-movement-og.jpg
description: A Python script that compares open and close spreads, totals and moneylines for every NFL game of the week using the Sports Odds API on RapidAPI.
---

# Track NFL betting line movement with Python

The [Sports Odds API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sports-odds-api) returns DraftKings odds for each NFL game with both the **open** and the **close** line. This script lists how far each spread, total and moneyline moved, and which games changed favourite.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /nfl/odds` and it needs no parameters. The response is `status`, `data` and `error`. In `data`, `lines` holds one entry per week (`displayValue`, `events`), and every event has `competitions[0].competitors` (with `homeAway`) and `competitions[0].odds[0]`. Inside the odds object, `pointSpread`, `total` and `moneyline` each have `open` and `close` values, for example `pointSpread.home.open.line`. Lines come as text such as `-16.5` or `o44.5`, so the script strips the `o` before converting. Full script: [`examples/sports_odds_line_movement.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/sports_odds_line_movement.py).

```python
data = call("/nfl/odds")
rows = moves(data["lines"][0])   # sorted by the size of the spread move
```

```bash
python sports_odds_line_movement.py
```

## Real output (20 Nov 2026)

```text
NFL Odds - Week 11 (12 games, odds from DraftKings)

Game         Day       Home spread   Move          Total   Move         Home ML
PIT @ PHI  11-22     -5.5 ->   +3.5     +9    42.5 ->  38.5     -4    -250 ->  +166
BAL @ CAR  11-22     +4.5 ->     -3   -7.5    46.5 ->  43.5     -3    +180 ->  -148
NYJ @ LAC  11-22     -9.5 ->     -3   +6.5    41.5 ->  41.5     +0    -440 ->  -169
ARI @ KC   11-22    -11.5 ->  -16.5     -5    44.5 ->  40.5     -4    -600 -> -1420
MIA @ BUF  11-22    -11.5 ->  -16.5     -5    47.5 ->  44.5     -3    -600 -> -1640
NO @ CHI   11-22     -6.5 ->  -11.5     -5    46.5 ->  48.5     +2    -278 ->  -600
JAX @ NYG  11-22     +1.5 ->     +6   +4.5    46.5 ->  46.5     +0    +105 ->  +210
CIN @ WSH  11-24     +1.5 ->     +6   +4.5    52.5 ->  53.5     +1    +105 ->  +241
TEN @ DAL  11-22     -6.5 ->   -8.5     -2    48.5 ->  54.5     +6    -290 ->  -381
LV @ DEN   11-22     -8.5 ->  -10.5     -2    41.5 ->  40.5     -1    -425 ->  -620
TB @ DET   11-22     -4.5 ->     -6   -1.5    49.5 ->  45.5     -4    -230 ->  -258
MIN @ SF   11-23     -3.5 ->   -3.5     +0    46.5 ->  46.5     +0    -205 ->  -172

Average spread move: 4.4 points. Favourite changed: PIT @ PHI, BAL @ CAR.
Biggest total move: TEN @ DAL (48.5 -> 54.5).
```

The spread moved by more than 4 points in 8 of the 12 games. The biggest swing is Pittsburgh at Philadelphia, where Philadelphia went from a 5.5-point favourite to a 3.5-point underdog. Baltimore at Carolina also changed favourite, from Carolina +4.5 to -3. Tennessee at Dallas has the biggest total move, up 6 points to 54.5.

## Things to know

- `lines` has two entries (Week 11 with 12 games and Week 12 with 16 games). The script reads the first one.
- Each game has exactly one odds provider, DraftKings.
- The call took about 3.4 seconds and returned about 226 KB.
- Several open lines are far from the close (Jets at Chargers opens at -9.5 and closes at -3). Check them against your sportsbook before you rely on them.
- Minnesota and San Francisco is labelled `MIN vs. SF` instead of `MIN @ SF`, but `homeAway` still says San Francisco is the home team.

## Ideas

- Store the output each hour and chart the spread against kick-off time.
- Alert yourself when a total moves by 3 points or more.
