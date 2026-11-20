"""Search Uniqlo and summarise prices, audience and the most reviewed items (Uniqlo Eccommerce API).

Usage:
    export RAPIDAPI_KEY=your_key
    python uniqlo_search_report.py jacket US
"""
import os
import statistics
import sys
import time
from collections import Counter

import requests

HOST = "uniqlo-eccommerce.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("error"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def price(p):
    """prices.promo is null for many products; fall back to prices.base."""
    pr = p["prices"]
    return (pr.get("promo") or pr["base"])["value"]


def report(query, country="US"):
    data = call("/search", query=query, countryIso=country, perPage=24, sortBy="featured")
    products = data["products"]
    prices = [price(p) for p in products]
    missing = sum(1 for p in products if not p["prices"].get("promo"))
    print(f"'{query}' in {country}: {data['pagination']['totalAvailable']} results, {len(products)} on this page")
    print(f"Price {min(prices):.2f} to {max(prices):.2f}, median {statistics.median(prices):.2f}; promo price missing on {missing}")
    print("Audience:", dict(Counter(p["genderName"] for p in products)))
    print("Related searches:", ", ".join(data["relatedKeywords"]), "\n")
    print(f"{'Most reviewed':<42}{'For':<8}{'Price':>7}{'Stars':>7}{'Reviews':>9}")
    for p in sorted(products, key=lambda p: -p["rating"]["count"])[:5]:
        print(f"{p['name'][:41]:<42}{p['genderName']:<8}{price(p):>7.2f}{p['rating']['average']:>7}{p['rating']['count']:>9,}")
    return products


if __name__ == "__main__":
    report(*(sys.argv[1:3] or ["jacket"]))
