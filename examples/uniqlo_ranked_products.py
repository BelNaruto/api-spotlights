"""Show Uniqlo's ranked products with ratings, review counts and colour choice (Uniqlo Eccommerce API).

Usage:
    export RAPIDAPI_KEY=your_key
    python uniqlo_ranked_products.py US 24
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
    pr = p["prices"]
    return (pr.get("promo") or pr["base"])["value"]


def ranked(country="US", limit=24):
    products = call("/product/ranked", countryIso=country, limit=limit)["products"]
    prices = [price(p) for p in products]
    reviews = sum(p["rating"]["count"] for p in products)
    stars = statistics.mean(p["rating"]["average"] for p in products)
    print(f"{len(products)} ranked products in {country}: price {min(prices):.2f} to {max(prices):.2f}, median {statistics.median(prices):.2f}")
    print(f"Average rating {stars:.2f} from {reviews:,} reviews; audience {dict(Counter(p['genderName'] for p in products))}\n")
    print(f"{'#':>2} {'Product':<42}{'For':<8}{'Price':>7}{'Stars':>7}{'Reviews':>9}{'Colours':>8}")
    for i, p in enumerate(products[:10], 1):
        print(f"{i:>2} {p['name'][:41]:<42}{p['genderName']:<8}{price(p):>7.2f}{p['rating']['average']:>7}"
              f"{p['rating']['count']:>9,}{len(p['colors']):>8}")
    return products


if __name__ == "__main__":
    args = sys.argv[1:]
    ranked(args[0] if args else "US", int(args[1]) if len(args) > 1 else 24)
