"""Show size-by-size stock, discount and review summary for one SHEIN product (Shein Data API).

Usage:
    export RAPIDAPI_KEY=your_key
    python shein_stock_and_reviews.py 59357445 US
"""
import os
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


def snapshot(goods_id, country="US"):
    price = call("/product/price", goods_id=goods_id, country=country)
    reviews = call("/product/reviews", goods_id=goods_id, country=country)
    p = price["price"]
    print(f"Product {price['goods_id']}: {p['retail']['display']} -> {p['sale']['display']} ({p['discount_percent']}% off)")
    print(f"Top-level stock field: {price['stock']}, sum of SKUs: {sum(s['stock'] or 0 for s in price['skus'])}\n")
    print(f"{'Size':<6}{'Stock':>6}  In stock")
    for s in price["skus"]:
        size = next((a["value"] for a in s["attributes"] if a["name"] == "Size"), "-")
        print(f"{size:<6}{s['stock']:>6}  {s['in_stock']}")
    summary = reviews["summary"]
    print(f"\nRating {summary['average']} from {summary['total']} reviews ({summary['total_display']}), {len(reviews['reviews'])} returned")
    for r in reviews["reviews"]:
        print(f"  {r['rating']}/5  {r['date']}  {r['color']} {r['size']}  {(r['content'] or '')[:60]}")
    return price, reviews


if __name__ == "__main__":
    args = sys.argv[1:]
    snapshot(args[0] if args else "59357445", args[1] if len(args) > 1 else "US")
