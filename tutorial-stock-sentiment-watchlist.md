---
title: Rank a stock watchlist by news sentiment and see where it comes from with Python
image: /assets/stock-sentiment-watchlist-og.jpg
description: A Python script that ranks up to 5 tickers with one call to the Stock Sentiment Analysis API on RapidAPI, then breaks one ticker down by news source and StockTwits mood.
---

# Rank a stock watchlist by news sentiment

The [Stock Sentiment Analysis API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/stock-sentiment-analysis) can compare up to 5 tickers in one request. This script ranks a watchlist, then looks inside one ticker: sentiment by news source, the StockTwits mood, and how many of the "top" headlines really mention the company.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

`GET /compare?symbols=AAPL,MSFT,TSLA,NVDA,AMZN` returns `ranking`, `mostPositive`, `mostNegative` and a `results` list with `sentimentIndex` and `distributionPercent` for each ticker. `GET /stock/{symbol}/sentiment?includeSocial=true` returns `bySource`, `topPositive`, `topNegative` and a `social` summary from StockTwits. Full script: [`examples/stock_sentiment_watchlist.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/stock_sentiment_watchlist.py).

```python
cmp = call("/compare", symbols="AAPL,MSFT,TSLA,NVDA,AMZN")
print(cmp["ranking"])   # most to least positive
```

```bash
python stock_sentiment_watchlist.py AAPL,MSFT,TSLA,NVDA,AMZN AAPL
```

## Real output (20 Nov 2026)

```
rank  symbol  index  positive  negative  articles
   1  AMZN     24.7     36.8%     12.1%       340  ############
   2  AAPL     16.9     38.2%     21.3%       338  ########
   3  MSFT     11.1     35.2%     24.1%       332  #####
   4  TSLA        9     32.7%     23.8%       324  ####
   5  NVDA     -6.5     30.2%     36.7%       341  
Most positive AMZN, most negative NVDA, spread 31.2 index points

AAPL (Apple Inc.): index 16.9, 338 articles

By source (sorted by index):
  businessinsider    50 articles  index    46  very positive
  seekingalpha       10 articles  index    40  very positive
  nasdaq             13 articles  index  38.5  positive
  yahoo              20 articles  index    20  positive
  newsapi            95 articles  index  14.7  positive
  google             52 articles  index   9.6  neutral
  finviz             93 articles  index   2.2  neutral
  investing           5 articles  index     0  neutral
Gap between businessinsider and investing: 46.0 points

StockTwits: 30 posts, only 11 tagged bullish or bearish (1 bull / 10 bear)
  bullBearIndex -81.8, but our model scores the post text as negative (index -10)

Top headlines that mention the company (or its ticker):
  topPositive: 3 of 5 mention AAPL
  topNegative: 3 of 5 mention AAPL
```

Amazon leads and Nvidia is the only ticker with more negative than positive articles. Inside Apple, the same news gets very different scores depending on the source: Business Insider is at +46 and Finviz at +2.2, a gap of 46 points. Finviz and NewsAPI supply the most articles, so they decide most of the overall index.

## Things to know

- The StockTwits summary here is based on 11 tagged posts out of 30. `bullBearIndex` ignores the 19 untagged posts, so -81.8 comes from 1 bullish and 10 bearish tags. Read `messageCount` and the tag counts before relying on it.
- The `topPositive` and `topNegative` lists are not always about the ticker. For Apple, 2 of the 5 top positive items were about other companies or ETFs, and 2 of the 5 top negative items were about another company or the whole market.
- Each article is scored with a word list, so a headline can be misread. Aggregates over hundreds of articles are more reliable than any single headline.
- `/compare` took about 25 seconds and `/sentiment` about 23 seconds in the playground, so run them from a scheduled job and cache the results.
- Sentiment measures the tone of the news and is not financial advice.

## Ideas

- Save the ranking every day and plot how the order changes.
- Drop the sources that return fewer than 10 articles before comparing tickers.
