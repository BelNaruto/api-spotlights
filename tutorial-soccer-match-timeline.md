---
title: Build a match timeline with goals, cards and substitutions in Python
image: /assets/soccer-match-timeline-og.jpg
description: A Python script that prints a minute-by-minute timeline of any football match with goals, assists, cards and substitutions, using the Soccer Live Info API on RapidAPI.
---

# Build a football match timeline in Python

Take any match id and print the full story of the game: goals with the running score, assists, cards and substitutions. It uses the [Soccer / Football Live Info API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/soccer-football-live-info).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

Match ids come from `GET /matches?date=...`. The endpoint `GET /matches/{matchId}/events` returns the `match`, a short list of `keyEvents` and the full `events` list, **newest first**, so the script reverses it. Full script: [`examples/soccer_match_timeline.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/soccer_match_timeline.py).

```python
data = call("/matches/aVUGdLT3lNb2iCEqFHhBv/events")
for e in reversed(data["events"]):
    print(e["type"], e.get("period"))
```

```bash
python soccer_match_timeline.py aVUGdLT3lNb2iCEqFHhBv
```

## Real output: Washington Spirit 2-1 Utah Royals (NWSL playoff semi-final, 14 Nov 2026)

| Minute | Event |
|--------|-------|
| 2' | GOAL Utah Royals: C. Lacasse (0-1) |
| 8' | GOAL Washington Spirit: S. Cantore (1-1), assist T. Rodman |
| HT | Half time |
| 52' | SUB Utah: C. Delzer on, M. Hammond off |
| 56' | GOAL Washington Spirit: C. Luvanga (2-1) |
| 63' | SUB Utah: M. Tanaka on, P. Cronin off |
| 71' | YELLOW CARD Utah: M. Tanaka |
| 74' | SUB Washington: T. Bolt on, S. Cantore off |
| 74' | SUB Washington: M. Ngock on, L. Santos off |
| 81' | SUB Utah: B. Mozingo on, J. Joseph off |
| 81' | SUB Utah: K. Simmonds on, M. Moriya off |
| 90+4' | YELLOW CARD Washington: T. Rodman |

Utah scored after two minutes, Washington levelled on 8' and won it with Luvanga's goal on 56'. The events list also contains period markers (first half, half time, second half, match end), which the script prints as plain labels.

## Ideas

- Combine it with the [match day summary](tutorial-soccer-matchday-summary.html) to print a timeline for the biggest game of the day.
- Count substitutions per team to see who used their bench early.
