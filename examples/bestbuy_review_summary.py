"""Summarise what Best Buy customers like and dislike about a product (BestBuy USA API).

Usage:
    export RAPIDAPI_KEY=your_key
    python bestbuy_review_summary.py 6501022
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


def summary(sku):
    d = call("/product/review/summary", skuId=sku)
    stats, dist = d["overallStats"], d["distributions"]
    total = sum(x["count"] for x in dist["ratings"])
    print(f"SKU {d['sku']}: {stats['averageOverallRating']} stars from {stats['totalReviewCount']:,} reviews, "
          f"{stats['recommendedPercent']}% recommend, top rated: {stats['topRated']}")
    print(f"Verified purchases: {d['verifiedPurchaseCount']:,}\n")
    print("Star distribution:")
    for x in sorted(dist["ratings"], key=lambda x: -x["value"]):
        print(f"  {x['value']} stars  {x['count']:>5}  {x['roundedPercent']:>3}%  " + "#" * round(x["roundedPercent"] / 4))
    print("\nWhat people like:")
    for x in dist["pros"]:
        print(f"  {x['value']:<14}{x['count']:>5} mentions")
    print("What people dislike:")
    for x in dist["cons"]:
        print(f"  {x['value']:<14}{x['count']:>5} mentions")
    print(f"\nRatings counted: {total:,}")
    return d


if __name__ == "__main__":
    summary(sys.argv[1] if len(sys.argv) > 1 else "6501022")
