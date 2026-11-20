"""Price ladder for any Zara search: price range and median per product family (Zara Data API).

Usage:
    export RAPIDAPI_KEY=your_key
    python zara_price_ladder.py jacket WOMAN
"""
import os
import statistics
import sys
import time
from collections import defaultdict

import requests

HOST = "zara-data-api.p.rapidapi.com"
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


def price_ladder(query, section="WOMAN", per_page=36):
    data = call("/search", query=query, section=section, perPage=per_page, language="en_US")
    products = data["products"]
    seen, families = set(), defaultdict(list)
    for p in products:
        c = p["content"]
        if c["reference"] in seen:  # the API can repeat a product in one page
            continue
        seen.add(c["reference"])
        families[c["familyName"]].append((c["pricing"]["value"], c["name"]))
    total = data["pagination"]["totalResults"]
    print(f"'{query}' in {section}: {total} results, {len(products)} returned, {len(seen)} unique\n")
    print(f"{'Family':<18}{'Items':>6}{'Min':>8}{'Median':>8}{'Max':>8}")
    for fam, rows in sorted(families.items(), key=lambda kv: -len(kv[1])):
        prices = [v for v, _ in rows]
        print(f"{fam:<18}{len(prices):>6}{min(prices):>8.1f}{statistics.median(prices):>8.1f}{max(prices):>8.1f}")
    print("\nPrices have no currency field; they are in the store of the language/country you query.")
    return families


if __name__ == "__main__":
    price_ladder(sys.argv[1] if len(sys.argv) > 1 else "jacket", sys.argv[2] if len(sys.argv) > 2 else "WOMAN")
