"""Rank YouTube search results by views and views per minute (YouTube Data API on RapidAPI).

Uses GET /search/ with a query. The result list mixes videos, shorts, shelves and channels, so the
script counts each type and ranks only the `singleVideo` items.

Usage:
    export RAPIDAPI_KEY=your_key
    python youtube_search_report.py "mr beast"
"""
import os
import sys
import time
from collections import Counter

import requests

HOST = "youtube-data19.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("message"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def videos(results):
    out = []
    for item in results:
        if item["type"] != "singleVideo":
            continue
        c = item["content"]
        views = int(c["views"]["text"].split()[0].replace(",", ""))
        secs = c["duration"]["seconds"]
        out.append({"title": c["title"], "channel": c["author"]["name"], "age": c["published"]["text"],
                    "secs": secs, "views": views, "vpm": views / (secs / 60) if secs else 0})
    return out


def report(data):
    results = data["results"]["results"]
    print(f"Query '{data['query']}', about {data['pagination']['estimatedResults']:,} results")
    print("Result types:", ", ".join(f"{k} {v}" for k, v in Counter(r["type"] for r in results).items()))
    vids = videos(results)
    print(f"\nTop 5 videos by views ({len(vids)} videos on the page)")
    for v in sorted(vids, key=lambda v: -v["views"])[:5]:
        print(f"  {v['views']:>12,}  {v['age']:>7}  {v['title'][:24]}")
    print("\nTop 5 by views per minute of video")
    for v in sorted(vids, key=lambda v: -v["vpm"])[:5]:
        print(f"  {v['vpm']:>12,.0f}  {v['secs'] // 60:>3} min  {v['title'][:24]}")
    total = sum(v["views"] for v in vids)
    print(f"\nTotal views of the {len(vids)} videos: {total:,} (average {total // len(vids):,})")


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "mr beast"
    report(call("/search/", query=q, sortBy="relevance", type="all", duration="all", uploadDate="all"))
