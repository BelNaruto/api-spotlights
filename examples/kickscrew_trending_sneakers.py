"""Trending sneakers leaderboard: demand score and sell-out risk for a collection.

Usage:
    export RAPIDAPI_KEY=your_key
    python kickscrew_trending_sneakers.py air-jordan 5
"""
import os
import sys
import time

import requests

HOST = "kickscrew-sneakers-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("error"):
                raise RuntimeError(body["error"])
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def trending(collection, limit=5):
    data = call(f"/v2/collections/{collection}/trending", limit=limit, scanSize=100)
    print(f"Collection: {data['collection']}  (scanned {data['scanned']} products)\n")
    print(f"{'#':<3}{'Product':<52}{'Price':>9}{'Score':>7}{'Risk':>8}{'Sizes':>8}")
    for i, p in enumerate(data["trending"], 1):
        sizes = f"{p['availableSizes']}/{p['totalSizes']}"
        print(f"{i:<3}{p['title'][:50]:<52}{p['lowestPrice']:>9.2f}{p['demandScore']:>7}{p['sellOutRisk']:>8}{sizes:>8}")
    return data


if __name__ == "__main__":
    trending(sys.argv[1] if len(sys.argv) > 1 else "air-jordan", int(sys.argv[2]) if len(sys.argv) > 2 else 5)
