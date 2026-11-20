"""Rank a watchlist by news sentiment and look inside one ticker (Stock Sentiment Analysis API).

Uses GET /compare for 2-5 tickers (one request), then GET /stock/{symbol}/sentiment for the detail:
sentiment by news source, the StockTwits mood and how many top headlines actually mention the company.

Usage:
    export RAPIDAPI_KEY=your_key
    python stock_sentiment_watchlist.py AAPL,MSFT,TSLA,NVDA,AMZN AAPL
"""
import os
import sys
import time

import requests

HOST = "stock-sentiment-analysis.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("error"))
            return body
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def show_ranking(cmp):
    rows = {r["symbol"]: r for r in cmp["results"]}
    print("rank  symbol  index  positive  negative  articles")
    for i, sym in enumerate(cmp["ranking"], 1):
        r = rows[sym]
        d = r["distributionPercent"]
        bar = "#" * max(0, int(r["sentimentIndex"] / 2))
        print(f"{i:>4}  {sym:<6} {r['sentimentIndex']:>6}  {d['positive']:>7}%  {d['negative']:>7}%  {r['articleCount']:>8}  {bar}")
    spread = rows[cmp["mostPositive"]]["sentimentIndex"] - rows[cmp["mostNegative"]]["sentimentIndex"]
    print(f"Most positive {cmp['mostPositive']}, most negative {cmp['mostNegative']}, spread {spread:.1f} index points")


def show_detail(data):
    s = data["sentiment"]
    print(f"\n{data['symbol']} ({data['company']['name']}): index {s['sentimentIndex']}, {s['articleCount']} articles")
    print("\nBy source (sorted by index):")
    sources = sorted(data["bySource"].items(), key=lambda kv: kv[1]["sentimentIndex"], reverse=True)
    for name, v in sources:
        print(f"  {name:<16} {v['articleCount']:>4} articles  index {v['sentimentIndex']:>5}  {v['label']}")
    top, low = sources[0], sources[-1]
    print(f"Gap between {top[0]} and {low[0]}: {top[1]['sentimentIndex'] - low[1]['sentimentIndex']:.1f} points")
    soc = data.get("social")
    if soc:
        tagged = soc["bullish"] + soc["bearish"]
        print(f"\nStockTwits: {soc['messageCount']} posts, only {tagged} tagged bullish or bearish "
              f"({soc['bullish']} bull / {soc['bearish']} bear)")
        print(f"  bullBearIndex {soc['bullBearIndex']}, but our model scores the post text as {soc['textSentiment']['label']} "
              f"(index {soc['textSentiment']['sentimentIndex']})")
    name = data["company"]["name"].split()[0].lower()
    print("\nTop headlines that mention the company (or its ticker):")
    for label in ("topPositive", "topNegative"):
        items = data[label]
        hits = [a for a in items if name in a["title"].lower() or data["symbol"].lower() in a["title"].lower()]
        print(f"  {label}: {len(hits)} of {len(items)} mention {data['symbol']}")


if __name__ == "__main__":
    symbols = sys.argv[1] if len(sys.argv) > 1 else "AAPL,MSFT,TSLA,NVDA,AMZN"
    detail = sys.argv[2] if len(sys.argv) > 2 else symbols.split(",")[0]
    show_ranking(call("/compare", symbols=symbols))
    show_detail(call(f"/stock/{detail}/sentiment", includeSocial="true"))
