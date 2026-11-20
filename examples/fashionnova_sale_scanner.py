"""Scan Fashion Nova search results for sale prices and verify the discounts (Fashion Nova API).

Usage:
    export RAPIDAPI_KEY=your_key
    python fashionnova_sale_scanner.py dress
"""
import os
import statistics
import sys
import time

import requests

HOST = "fashion-nova-api.p.rapidapi.com"
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


def scan(query, per_page=20):
    data = call("/search", query=query, perPage=per_page, sortBy="RELEVANCE", country="US")
    products = data["products"]
    sale = [p for p in products if p["price"]["onSale"]]
    prices = [p["price"]["amount"] for p in products]
    print(f"'{query}': {data['pagination']['totalAvailable']} results, {len(products)} on this page, {len(sale)} on sale")
    print(f"Price {min(prices):.2f} to {max(prices):.2f}, median {statistics.median(prices):.2f} {products[0]['price']['currency']}")
    if sale:
        avg = statistics.mean(p["price"]["discountPercentage"] for p in sale)
        print(f"Average discount {avg:.1f}%\n")
    wrong = 0
    print(f"{'Product':<42}{'Now':>7}{'Was':>8}{'Off':>5}")
    for p in sorted(sale, key=lambda p: -p["price"]["discountPercentage"])[:8]:
        pr = p["price"]
        expected = round((1 - pr["amount"] / pr["compareAt"]) * 100)
        wrong += expected != pr["discountPercentage"]
        print(f"{p['title'][:41]:<42}{pr['amount']:>7.2f}{pr['compareAt']:>8.2f}{pr['discountPercentage']:>4}%")
    print(f"\nDiscount percentages that do not match the prices: {wrong}")
    return products


if __name__ == "__main__":
    scan(sys.argv[1] if len(sys.argv) > 1 else "dress")
