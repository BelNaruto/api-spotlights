---
title: Build a Serie A table with points per game and goal difference in Python
image: /assets/seriea-table-report-og.jpg
description: A Python script that reads the Serie A table with the Serie A API on RapidAPI and prints wins, draws, goal difference, points per game and the European and relegation zones.
---

# Serie A table with points per game and goal difference

The [Serie A API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/serie-a-api1) returns the full league table with `GET /tables?season=2025` (season 2025 is 2025-26). This script turns it into a readable table and adds points per game, because the `ppg` field comes back as 0.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

Each team in `children[0].standings.entries` has a `stats` list of name and value pairs (`wins`, `ties`, `pointsFor`, `points`, `rank`). The script turns it into a dictionary, calculates goal difference and points per game, and prints the zone from the `note` field. Full script: [`examples/seriea_table_report.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/seriea_table_report.py).

```python
s = {x["name"]: x["value"] for x in e["stats"]}
ppg = s["points"] / s["gamesPlayed"]
```

```bash
python seriea_table_report.py 2025
```

## Real output (20 Nov 2026)

```
2025-26 Italian Serie A
 # team              P   W  D  L  GF  GA   GD  pts   ppg  zone
 1 Internazionale   38  27  6  5  89  35  +54   87  2.29  Champions League
 2 Napoli           38  23  7  8  58  36  +22   76  2.00  Champions League
 3 AS Roma          38  23  4 11  59  31  +28   73  1.92  Champions League
 4 Como             38  20 11  7  65  29  +36   71  1.87  Champions League
 5 AC Milan         38  20 10  8  53  35  +18   70  1.84  Europa League
 6 Juventus         38  19 12  7  61  34  +27   69  1.82  Europa League
 7 Atalanta         38  15 14  9  51  36  +15   59  1.55  Conference League qualifying
 8 Bologna          38  16  8 14  49  46   +3   56  1.47  
 9 Lazio            38  14 12 12  41  40   +1   54  1.42  
10 Udinese          38  14  8 16  45  48   -3   50  1.32  
11 Sassuolo         38  14  7 17  46  50   -4   49  1.29  
12 Torino           38  12  9 17  44  63  -19   45  1.18  
13 Parma            38  11 12 15  28  46  -18   45  1.18  
14 Cagliari         38  11 10 17  40  53  -13   43  1.13  
15 Fiorentina       38   9 15 14  41  50   -9   42  1.11  
16 Genoa            38  10 11 17  41  51  -10   41  1.08  
17 Lecce            38  10  8 20  28  50  -22   38  1.00  
18 Cremonese        38   8 10 20  32  57  -25   34  0.89  Relegated
19 Hellas Verona    38   3 12 23  25  61  -36   21  0.55  Relegated
20 Pisa             38   2 12 24  26  71  -45   18  0.47  Relegated

Best goal difference: Internazionale (+54)
```

Inter won the 2025-26 table by 11 points, and Como finished in the Champions League places in 4th. Como had the best defence with 29 goals conceded, Pisa the worst with 71.

## Things to know

- In this API, `pointsFor` and `pointsAgainst` are goals scored and conceded, and `ties` is draws.
- The playground lists this endpoint as `Get News`, and `Get Standings` returns only season details, not a table. Use `/tables`.
- `season=2025` is the 2025-26 season. `season=2024` gives 2024-25.

## Ideas

- Compare the table of two seasons to see which teams moved most.
- Mark the points gap between each zone to show how close the race was.
