---
title: Check how much news is behind a stock's sentiment trend with Python
image: /assets/stock-sentiment-timeline-coverage-og.jpg
description: A Python script that reads the daily sentiment timeline from the Stock Sentiment Analysis API on RapidAPI and shows how many articles stand behind each day and the momentum value.
---

# Check how much news is behind a stock's sentiment trend

The sentiment timeline gives one number per day, and a `trend` label such as `improving`. A day with 1 article and a day with 161 articles look the same in that label. This script uses the [Stock Sentiment Analysis API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/stock-sentiment-analysis) to print the timeline together with the article count behind each day, so you can see which days to trust.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /stock/{symbol}/sentiment/timeline` with `days` (1 to 30). It returns `overall`, `momentum`, `trend` and a `timeline` list with one row per day, including days with no news. Each row has `articleCount`, `sentimentIndex` (from -100 to +100), `label` and a `distribution` of positive, neutral and negative articles. The script marks days with fewer than 10 articles as thin and recomputes the index for each half of the window, weighted by article count. Full script: [`examples/stock_sentiment_timeline_coverage.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/stock_sentiment_timeline_coverage.py).

```python
data = call("/stock/MSFT/sentiment/timeline", days=14)
thin = [d["date"] for d in data["timeline"] if d["articleCount"] < 10]
```

```bash
python stock_sentiment_timeline_coverage.py MSFT 14
```

## Real output (20 Nov 2026)

```
MSFT  2026-11-07 -> 2026-11-20  326 articles
API says: index 9.2, momentum 66.1, trend improving

date   articles  index  mood
11-07        0       -  neutral        thin
11-08        0       -  neutral        thin
11-09        0       -  neutral        thin
11-10        3   -33.3  negative       thin
11-11        1  -100.0  very negative  thin
11-12        0       -  neutral        thin
11-13        0       -  neutral        thin
11-14        1  -100.0  very negative  thin
11-15        0       -  neutral        thin
11-16       21     0.0  neutral      #####
11-17       32   -15.6  negative     ########
11-18       64    32.8  positive     ################
11-19      161     9.3  neutral      ########################################
11-20       43     4.7  neutral      ##########

Days without news: 6 of 14. Days under 10 articles: 9.
First half: 4 articles, index -50.0
Second half: 322 articles, index 9.9
Only days with 10+ articles: 5 days, index 10.3
Share of all articles in the last 4 days: 92%
```

The API reports `momentum 66.1` and `improving` for Microsoft. The table shows why that needs care: the first half of the window holds 4 articles in total, and 3 of them were negative, so the "improvement" compares a handful of headlines with 322 articles. The 5 days that have real coverage sit between -15.6 and +32.8 and average about +10.

## Things to know

- The news sources only keep recent articles, so older days are almost empty. Using `days=30` mostly adds empty rows.
- Days without articles come back with `sentimentIndex` 0 and the label `neutral`. Check `articleCount` before treating that as a real reading.
- Thin days can show extreme values, for example -100 from a single article.
- One call took about 24 seconds in the playground, so cache the result. News is refreshed about every 15 minutes.
- Sentiment measures the tone of the news, not future price, and it is not financial advice.

## Ideas

- Only alert when `trend` changes **and** both halves have at least 30 articles.
- Run it for a few tickers every morning and save the rows to a CSV to build your own history, since the API only looks back 30 days.
