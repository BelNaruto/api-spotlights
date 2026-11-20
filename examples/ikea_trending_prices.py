"""Take IKEA's trending searches and check live prices for each (IKEA Data API).

Usage:
    export RAPIDAPI_KEY=your_key
    python ikea_trending_prices.py
"""
import os
import time

import requests

HOST = "ikea-data-api.p.rapidapi.com"
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


def trending_prices():
    trend = call("/search/trending")
    print("Trending categories:", ", ".join(c["name"] for c in trend["categories"]), "\n")
    print(f"{'Search':<18}{'Results':>8}{'Min':>9}{'Max':>9}  Cheapest item")
    for s in trend["searchSuggestions"]:
        data = call("/search", query=s["text"], type="normal", perPage=24)
        products = data["items"]["products"]
        if not products:
            print(f"{s['text']:<18}{0:>8}")
            continue
        cheapest = min(products, key=lambda p: p["salesPrice"]["numeral"])
        prices = [p["salesPrice"]["numeral"] for p in products]
        print(f"{s['text']:<18}{data['pagination']['totalAvailable']:>8}{min(prices):>9.2f}{max(prices):>9.2f}  "
              f"{cheapest['name']} ({cheapest['typeName']})")
    print("\nThe cheapest hit is often a spare part (a leg, an insert), so check typeName.")
    return trend


if __name__ == "__main__":
    trending_prices()
