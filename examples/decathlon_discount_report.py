"""Which Decathlon new arrivals are on sale, and how much stock is left (Decathlon API on RapidAPI).

Reads a collection with GET /collection/products. Each product has variants (sizes) with `price`,
`compare_at_price` and `available`. The script finds the discount for each product and how many sizes are in stock.

Usage:
    export RAPIDAPI_KEY=your_key
    python decathlon_discount_report.py new-arrivals
"""
import os
import sys
import time
from collections import defaultdict

import requests

HOST = "decathlon-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("message"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def summarize(p):
    prices = [float(v["price"]) for v in p["variants"]]
    was = [float(v["compare_at_price"]) for v in p["variants"] if v.get("compare_at_price")]
    price, old = min(prices), max(was) if was else 0
    return {
        "title": p["title"], "vendor": p["vendor"], "price": price, "was": old,
        "discount": round((1 - price / old) * 100) if old > price else 0,
        "sizes": len(p["variants"]), "in_stock": sum(1 for v in p["variants"] if v["available"]),
    }


def report(products):
    rows = [summarize(p) for p in products]
    sale = [r for r in rows if r["discount"]]
    print(f"{len(rows)} products, {len(sale)} with a compare_at_price above the price")
    print(f"Average discount on those: {sum(r['discount'] for r in sale) / len(sale):.0f}%\n")
    print("Biggest discounts:")
    for r in sorted(sale, key=lambda r: -r["discount"])[:5]:
        print(f"  -{r['discount']}%  {r['price']:>6.2f} (was {r['was']:.2f})  {r['title']}")
    by_vendor = defaultdict(list)
    for r in rows:
        by_vendor[r["vendor"]].append(r)
    print("\nBy brand:   products  on sale  sizes in stock")
    for v, items in sorted(by_vendor.items(), key=lambda kv: -len(kv[1])):
        sizes, stock = sum(i["sizes"] for i in items), sum(i["in_stock"] for i in items)
        print(f"  {v:<10} {len(items):>8}  {sum(1 for i in items if i['discount']):>7}  {stock}/{sizes}")
    low = [r for r in rows if r["in_stock"] < r["sizes"] / 2]
    print(f"\nProducts with less than half the sizes in stock: {len(low)}")
    for r in low:
        print(f"  {r['in_stock']}/{r['sizes']}  {r['title']}")


if __name__ == "__main__":
    report(call("/collection/products", collectionsHandle=sys.argv[1] if len(sys.argv) > 1 else "new-arrivals", page=1, country="us"))
