"""Summarise an ASOS search: prices, brands and items selling fast (Asos API).

Usage:
    export RAPIDAPI_KEY=your_key
    python asos_search_snapshot.py jacket
"""
import collections
import os
import statistics
import sys
import time

import requests

HOST = "asos-api6.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def snapshot(query):
    data = call("/product/search", query=query)
    items = data["products"]
    prices = sorted(p["price"]["current"]["value"] for p in items if p["price"]["current"]["value"] is not None)
    brands = collections.Counter(p["brandName"] for p in items)
    marked_down = [p for p in items if p["price"]["isMarkedDown"]]
    print(f"'{data['searchTerm']}': {data['itemCount']:,} results, {len(items)} returned")
    print(f"Price: min {prices[0]}, median {statistics.median(prices)}, max {prices[-1]} {items[0]['price']['currency']}")
    print(f"Marked down: {len(marked_down)}, selling fast: {sum(p['isSellingFast'] for p in items)}, "
          f"restocking soon: {sum(p['isRestockingSoon'] for p in items)}")
    print(f"{len(brands)} brands. Most common: " + ", ".join(f"{b} {n}" for b, n in brands.most_common(5)))
    print("\nCheapest three:")
    for p in sorted(items, key=lambda p: p["price"]["current"]["value"])[:3]:
        print(f"  {p['price']['current']['text']:>8}  {p['brandName']:<14}{p['name'][:50]}")
    return items


if __name__ == "__main__":
    snapshot(sys.argv[1] if len(sys.argv) > 1 else "jacket")
