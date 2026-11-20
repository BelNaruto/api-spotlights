---
title: Rank YouTube search results by views per minute with Python
image: /assets/youtube-search-report-og.jpg
description: A Python script that runs a YouTube search with the YouTube Data API on RapidAPI, counts videos, shorts and channels, and ranks the videos by views and views per minute.
---

# Rank YouTube search results by views per minute

A YouTube search returns more than videos. The [YouTube Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/youtube-data19) gives you videos, shorts, shelves and channels in one list. This script keeps the videos and ranks them, so you can see which ones get the most views for their length.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /search/?query=mr beast` and reads the `results.results` list. Each item has a `type`; the script keeps `singleVideo`, turns the view text (`87,855,652 views`) into a number and divides by the length in minutes. Full script: [`examples/youtube_search_report.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/youtube_search_report.py).

```python
views = int(c["views"]["text"].split()[0].replace(",", ""))
vpm = views / (c["duration"]["seconds"] / 60)
```

```bash
python youtube_search_report.py "mr beast"
```

## Real output (20 Nov 2026)

Video titles are cut to 24 characters here.

```
Query 'mr beast', about 10,027,550 results
Result types: singleVideo 19, channel 1, shelf 2, shorts 3

Top 5 videos by views (19 videos on the page)
   617,479,247   3y ago  $1 vs $500,000 Plane Tic
   591,567,273   3y ago  $1 vs $100,000,000 Car!
   390,418,742   2y ago  I Survived 7 Days In An 
   354,953,298  1mo ago  Eat Everything In A Groc
   345,455,380   2y ago  Ages 1 - 100 Decide Who 

Top 5 by views per minute of video
    58,714,350   10 min  $1 vs $500,000 Plane Tic
    37,880,508   15 min  $1 vs $100,000,000 Car!
    28,100,093    4 min  I Cleaned The World’s Di
    28,028,711   10 min  Real Life Spider-Man Vs 
    26,202,600   14 min  I Survived 7 Days In An 

Total views of the 19 videos: 4,743,995,673 (average 249,683,982)
```

The two $1 videos lead in both rankings. A 4-minute video climbs to third place once length is taken into account.

## Things to know

- The page holds 25 items but only 19 are videos. Shorts, shelves and the channel card have a different shape, so filter on `type`.
- `published.text` is relative (`5d ago`, `3y ago`), not a date. Use it as a rough age only.
- `pagination.isNextPageAvailable` tells you if there is another page.

## Ideas

- Add `uploadDate` or `duration` filters to compare recent videos only.
- Save each run to a CSV to follow how the ranking moves.
