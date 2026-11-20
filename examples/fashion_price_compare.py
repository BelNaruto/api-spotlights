"""Compare prices for one search term across many fashion retailers (Fashion Product API).

Usage:
    export RAPIDAPI_KEY=your_key
    python fashion_price_compare.py jacket
"""
import os
import statistics
import sys
import time
from collections import defaultdict

import requests

HOST = "fashion-product-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            if body.get("error"):
                raise RuntimeError(body["error"])
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def compare(query):
    data = call("/products/search/all", q=query)
    print(f"{data['count']} products for '{query}'\n")
    by_retailer = defaultdict(list)
    for p in data["results"]:
        if p.get("price") and p["price"].get("amount") is not None:
            by_retailer[p["retailer"]].append((p["price"]["amount"], p["price"]["currency"]))
    print(f"{'Retailer':<18}{'Items':>6}{'Median':>10}{'Average':>10}  Currency")
    for name, prices in sorted(by_retailer.items(), key=lambda kv: statistics.median(a for a, _ in kv[1])):
        amounts = [a for a, _ in prices]
        cur = "/".join(sorted({c for _, c in prices}))
        print(f"{name:<18}{len(amounts):>6}{statistics.median(amounts):>10.2f}{statistics.mean(amounts):>10.2f}  {cur}")
    print("\nPrices are in each retailer's own currency (no conversion).")
    for r in data["retailers"]:
        if not r["available"]:
            print(f"Unavailable: {r['retailer']}: {r['reason'][:90]}")
    return by_retailer


if __name__ == "__main__":
    compare(sys.argv[1] if len(sys.argv) > 1 else "jacket")
