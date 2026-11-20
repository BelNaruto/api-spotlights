---
title: Recap any Champions League matchday with Python
image: /assets/uefa-matchday-recap-og.jpg
description: A Python script that recaps a Champions League matchday with scores, goals, penalties, cards, attendance and multi-goal scorers, using the UEFA Champions League API on RapidAPI.
---

# Recap any Champions League matchday with Python

Give the script a date and it prints that day's scores and totals for goals, cards and crowds. It uses the [UEFA Champions League API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/uefa-champions-league1).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /scoreboard` with `year` (required), `month` and `day` (two digits) and `limit`. The matches are in `scoreboard.events`. Each has `competitions[0]` with `competitors` (`homeAway`, `score`, `team`), `status`, `attendance` and a `details` list of events: goals (`scoringPlay`, `penaltyKick`, `ownGoal`), `yellowCard`, `redCard` and `athletesInvolved`. Full script: [`examples/uefa_matchday_recap.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/uefa_matchday_recap.py).

```python
events = call("/scoreboard", year=2026, month="01", day="28")["scoreboard"]["events"]
for e in events:
    c = e["competitions"][0]
    print([(t["team"]["shortDisplayName"], t["score"]) for t in c["competitors"]])
```

```bash
python uefa_matchday_recap.py 2026 01 28
```

## Real output (20 Nov 2026)

28 January 2026, the last league-phase matchday: **18 matches, all Full Time, 61 goals (3.39 per match), 5 penalties, 67 yellow cards, 4 red cards**. Total attendance was 772,602, from 5,109 at Pafos to 81,365 at Dortmund.

| Match | Score | Attendance |
|-------|-------|-----------|
| Liverpool v FK Qarabag | 6-0 | 60,043 |
| Benfica v Real Madrid | 4-2 | 64,305 |
| Barcelona v København | 4-1 | 44,609 |
| Pafos v Slavia Prague | 4-1 | 5,109 |
| Arsenal v Kairat Almaty | 3-2 | 50,200 |
| Athletic v Sporting | 2-3 | 52,065 |
| Napoli v Chelsea | 2-3 | 46,513 |
| Dortmund v Inter Milan | 0-2 | 81,365 |
| PSV v Bayern | 1-2 | 35,000 |
| Monaco v Juventus | 0-0 | 10,287 |

Five players scored twice: Malik Tillman, Kylian Mbappé, Andreas Schjelderup, Alexis Mac Allister and João Pedro.

## Things to know

- `venue.fullName` came back empty on these events, so do not rely on it for stadium names.
- The scoreboard path takes a date, not a matchday number, so look the date up in the schedule first.

## Ideas

- Run it every matchday and post the headline numbers to a channel.
- Join with the standings script to show which results changed a team's zone.
