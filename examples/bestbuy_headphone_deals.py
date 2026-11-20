"""Find the biggest Best Buy discounts for a search term (BestBuy USA API).

Usage:
    export RAPIDAPI_KEY=your_key
    python bestbuy_headphone_deals.py headphones
"""
import os
import sys
import time

import requests

HOST = "bestbuy-usa.p.rapidapi.com"
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


def deals(query):
    products = call("/search", query=query)["products"]
    priced = [p for p in products if p["price"] and p["price"]["customerPrice"] is not None]
    missing = [p["title"] for p in products if p not in priced]
    on_sale = [p for p in priced if p["price"]["previousPrice"] and p["price"]["customerPrice"] < p["price"]["previousPrice"]]

    def pct(p):
        return round((1 - p["price"]["customerPrice"] / p["price"]["previousPrice"]) * 100)

    print(f"'{query}': {len(products)} products, {len(priced)} with a price, {len(on_sale)} on sale")
    print(f"Average discount {sum(map(pct, on_sale)) / len(on_sale):.1f}%, total saved if you bought all: ${sum(p['price']['discount'] for p in on_sale):,.2f}\n")
    print("Biggest discounts:")
    for p in sorted(on_sale, key=pct, reverse=True)[:5]:
        pr = p["price"]
        print(f"  {pct(p):>3}%  ${pr['previousPrice']:>7} -> ${pr['customerPrice']:>7}  (save ${pr['discount']:.0f})  "
              f"{p['ratings']['score']} stars / {p['ratings']['count']}  {p['title'][:44]}")
    if missing:
        print(f"\nNo price returned for {len(missing)} products: " + "; ".join(t[:30] for t in missing))
    return on_sale


if __name__ == "__main__":
    deals(sys.argv[1] if len(sys.argv) > 1 else "headphones")
