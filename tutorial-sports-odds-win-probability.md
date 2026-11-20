---
title: Turn NFL moneylines and Super Bowl odds into win probabilities with Python
image: /assets/sports-odds-win-probability-og.jpg
description: A Python script that converts moneylines from the Sports Odds API on RapidAPI into fair win probabilities, measures the bookmaker margin and adds up the Super Bowl futures.
---

# Turn NFL moneylines into win probabilities with Python

American odds hide the probability behind them, and the bookmaker margin makes both sides add up to more than 100%. This script uses the [Sports Odds API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sports-odds-api) to convert the Week 11 moneylines into fair home win chances at the open and at the close, and to check the Super Bowl futures.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /nfl/odds`. Each event has `moneyline.home` and `moneyline.away` with `open.odds` and `close.odds` as text (`"-600"`, `"+440"`). The raw probability is `100 / (odds + 100)` for positive odds and `-odds / (-odds + 100)` for negative odds. Divide each raw value by the sum of both sides to remove the margin. The same response has `futures[0].future.books`, a list of teams with `displayValue` such as `"+500"`. Full script: [`examples/sports_odds_win_probability.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/sports_odds_win_probability.py).

```python
p_home, margin = fair_home("-600", "+440")   # 0.82 fair home win chance, 4.0% margin
```

```bash
python sports_odds_win_probability.py
```

## Real output (20 Nov 2026)

```text
NFL Odds - Week 11: fair home win chance, open vs close

Game       Home open Home close   Shift  Margin
PIT @ PHI       69%        36%    -32pt    4.0%
BAL @ CAR       34%        57%    +23pt    4.1%
CIN @ WSH       47%        28%    -19pt    4.0%
NYJ @ LAC       78%        60%    -18pt    4.1%
JAX @ NYG       47%        31%    -16pt    4.1%
NO @ CHI        71%        82%    +12pt    4.0%
MIA @ BUF       82%        91%     +8pt    4.1%
ARI @ KC        82%        90%     +8pt    4.1%
LV @ DEN        78%        83%     +5pt    4.1%
TEN @ DAL       71%        76%     +5pt    4.0%
MIN @ SF        64%        61%     -4pt    4.1%
TB @ DET        67%        69%     +2pt    4.0%

Average bookmaker margin on the closing moneyline: 4.1%

Super Bowl Winner futures (16 teams listed, market active: False)
  Buffalo Bills              +500   16.7%
  San Francisco 49ers        +500   16.7%
  Jacksonville Jaguars       +750   11.8%
  Chicago Bears              +850   10.5%
  Cincinnati Bengals         +950    9.5%
  Kansas City Chiefs         +970    9.3%
  Los Angeles Rams          +1200    7.7%
  Seattle Seahawks          +1500    6.2%
  Minnesota Vikings         +1500    6.2%
  Denver Broncos            +1600    5.9%
  Detroit Lions             +1800    5.3%
  Green Bay Packers         +4000    2.4%
  Houston Texans            +5000    2.0%
  Pittsburgh Steelers       +5500    1.8%
  Tampa Bay Buccaneers      +6500    1.5%
  New York Giants           +6500    1.5%
Listed teams add up to 115% before the other 16 teams.
```

The bookmaker margin is a steady 4.0% to 4.1% on every game. Philadelphia is the biggest mover: its fair win chance dropped from 69% to 36% between the open and the close, while Carolina went up from 34% to 57%.

## Things to know

- The futures list has only 16 teams and `active` is `false` for the Super Bowl market, so the prices may be stale.
- The 16 listed teams already add up to 115%. Adding the other 16 teams can only push the total higher, so these prices contain a large margin and are not true probabilities.
- Odds are returned as strings, not numbers.
- The `open` odds for several games are far from the `close` ones, so large shifts may reflect old opening prices.

## Ideas

- Compare these fair probabilities with your own model and print the games where you disagree by more than 10 points.
- Do the same for the other leagues in the API (NBA, NHL, MLB and more).
