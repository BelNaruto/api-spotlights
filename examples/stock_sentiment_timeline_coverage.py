"""Read the daily sentiment timeline of a stock and check how much news is behind each day (Stock Sentiment Analysis API).

The timeline returns one row per day, including days with no articles. This script marks thin days,
and compares the API's momentum with a version that only counts days that have enough articles.

Usage:
    export RAPIDAPI_KEY=your_key
    python stock_sentiment_timeline_coverage.py MSFT 14
"""
import os
import sys
import time

import requests

HOST = "stock-sentiment-analysis.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}
THIN = 10  # days with fewer articles than this are treated as thin


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


def index(days):
    """Net sentiment index (-100..100) over a list of day rows, weighted by article count."""
    pos = sum(d["distribution"]["positive"] for d in days)
    neg = sum(d["distribution"]["negative"] for d in days)
    total = sum(d["articleCount"] for d in days)
    return round((pos - neg) / total * 100, 1) if total else None


def report(data):
    days = data["timeline"]
    half = len(days) // 2
    first, second = days[:half], days[half:]
    print(f"{data['symbol']}  {data['from']} -> {data['to']}  {data['overall']['articleCount']} articles")
    print(f"API says: index {data['overall']['sentimentIndex']}, momentum {data['momentum']}, trend {data['trend']}\n")
    print("date   articles  index  mood")
    for d in days:
        bar = "#" * min(40, d["articleCount"] // 4)
        flag = "  thin" if d["articleCount"] < THIN else ""
        idx = f"{d['sentimentIndex']:>6}" if d["articleCount"] else "     -"
        print(f"{d['date'][5:]}  {d['articleCount']:>7}  {idx}  {d['label']:<13}{bar}{flag}")
    empty = sum(1 for d in days if d["articleCount"] == 0)
    thin = sum(1 for d in days if d["articleCount"] < THIN)
    print(f"\nDays without news: {empty} of {len(days)}. Days under {THIN} articles: {thin}.")
    a, b = index(first), index(second)
    print(f"First half: {sum(d['articleCount'] for d in first)} articles, index {a}")
    print(f"Second half: {sum(d['articleCount'] for d in second)} articles, index {b}")
    solid = [d for d in days if d["articleCount"] >= THIN]
    print(f"Only days with {THIN}+ articles: {len(solid)} days, index {index(solid)}")
    share = sum(d["articleCount"] for d in days[-4:]) / max(1, data["overall"]["articleCount"])
    print(f"Share of all articles in the last 4 days: {share:.0%}")


if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "MSFT"
    window = sys.argv[2] if len(sys.argv) > 2 else "14"
    report(call(f"/stock/{symbol}/sentiment/timeline", days=window))
