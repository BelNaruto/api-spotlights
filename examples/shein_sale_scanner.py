"""Scan a SHEIN search for the deepest discounts and the best-rated items (Shein Data API).

Usage:
    export RAPIDAPI_KEY=your_key
    python shein_sale_scanner.py dress US
"""
import os
import statistics
import sys
import time

import requests

HOST = "shein-data-api.p.rapidapi.com"
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


def scan(query, country="US", limit=20):
    data = call("/search/products", query=query, country=country, limit=limit)
    items = data["products"]
    prices = sorted(p["price"]["sale"]["usd_amount"] for p in items)
    discounts = [p["price"]["discount_percent"] for p in items if p["price"]["discount_percent"] is not None]
    print(f"'{query}' ({country}): {data['total']:,} results, {len(items)} returned")
    print(f"Price USD: min {prices[0]}, median {statistics.median(prices)}, max {prices[-1]}")
    print(f"Discounted: {len(discounts)}/{len(items)}, average {statistics.mean(discounts):.1f}%, max {max(discounts)}%")
    print(f"In stock: {sum(p['in_stock'] for p in items)}, quick ship: {sum(bool(p['quick_ship']) for p in items)}\n")
    print("Deepest discounts:")
    for p in sorted(items, key=lambda p: -p["price"]["discount_percent"])[:5]:
        print(f"  {p['price']['discount_percent']:>3}%  {p['price']['retail']['display']:>7} -> {p['price']['sale']['display']:>7}"
              f"  rating {p['rating']['average']}  {p['name'][:40]}")
    return items


if __name__ == "__main__":
    args = sys.argv[1:]
    scan(args[0] if args else "dress", args[1] if len(args) > 1 else "US")
