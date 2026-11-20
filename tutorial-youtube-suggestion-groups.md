---
title: Group YouTube search suggestions by topic with Python
image: /assets/youtube-suggestion-groups-og.jpg
description: A Python script that reads YouTube search suggestions with the YouTube Data API on RapidAPI and groups them by the next word to find content ideas.
---

# Find video ideas from YouTube search suggestions

When you type in the YouTube search box, it suggests what people search next. The [YouTube Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/youtube-data19) returns those suggestions, and this script groups them to show which topics are most common.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /search/suggestion?query=how to`, removes the seed from each suggestion and groups the rest by the first word that follows. Full script: [`examples/youtube_suggestion_groups.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/youtube_suggestion_groups.py).

```python
rest = s[len(seed):].split()
groups[rest[0]].append(" ".join(rest[1:]))
```

```bash
python youtube_suggestion_groups.py "how to"
```

## Real output (20 Nov 2026)

```
14 suggestions for 'how to'

draw      3  -; a turkey; a body
make      3  slime; a paper airplane; a squishy
do        2  the moonwalk; a backflip
play      2  gta 6 early on ps5; gta 6 early on xbox
crochet   1  for beginners
moonwalk  1  -
save      1  a life the fray
tie       1  a tie

Longest: how to play gta 6 early on xbox
```

Drawing and making things lead. Two suggestions are about playing GTA 6 early, one for each console, which shows a current trend.

## Things to know

- The API returns 14 suggestions for this query, with no scores or ranking numbers, so the order is the only signal.
- The same idea can appear twice (`how to moonwalk` and `how to do the moonwalk`). Group by the topic words if you need to merge them.
- Suggestions change over time and by day. Run the script again and compare.

## Ideas

- Try `how to a`, `how to b` and so on to build a longer list.
- Feed the groups into a content calendar for your channel.
