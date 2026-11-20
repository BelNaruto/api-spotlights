"""Break down the reviews of an AliExpress product by phone model, country and shipping method (AliExpress Data API).

Reads pages of GET /product/reviews, cleans the messy variant text in `sku`, and counts reviews by
model, buyer country and shipping option. It also compares the sample with the product rating block.

Usage:
    export RAPIDAPI_KEY=your_key
    python aliexpress_review_breakdown.py 3256807637171608 2
"""
import os
import re
import sys
import time
from collections import Counter, defaultdict

import requests

HOST = "aliexpress-data.p.rapidapi.com"
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


def model(sku):
    """'Material:For iPhone 15Pro Max ' and 'For iPhone 15 ProMax' both become '15 Pro Max'."""
    s = sku.replace("Material:", "").replace("For iPhone", "")
    s = re.sub(r"Ships From:\w+", "", s).strip()
    s = re.sub(r"(\d)(Pro|Plus|Mini)", r"\1 \2", s)
    s = re.sub(r"Pro\s*Max", "Pro Max", s)
    return s or "unknown"


def shipping(name):
    return name.replace("AliExpress Selection", "").replace("Aliexpress Selection", "").strip().title()


def report(data_pages):
    reviews = [r for page in data_pages for r in page["reviews"]]
    pg = data_pages[0]["pagination"]
    rating = data_pages[0]["rating"]
    n = len(reviews)
    avg = sum(r["rating"] for r in reviews) / n
    print(f"{n} reviews read ({pg['totalCount']} reviews in total, page size {pg['pageSize']})")
    print(f"Sample average {avg:.2f} stars, API rating block says {rating['average']} ({rating['averagePercent']}%)")
    counted = sum(v["count"] for v in rating["breakdown"].values())
    print(f"Rating breakdown counts {counted} ratings, pagination counts {pg['totalCount']} reviews")

    for title, key, top in (("Phone models", lambda r: model(r["sku"]), 8),
                            ("Buyer countries", lambda r: r["country"], 6),
                            ("Shipping", lambda r: shipping(r["logistics"]), 6)):
        print(f"\n{title}:")
        for name, c in Counter(key(r) for r in reviews).most_common(top):
            print(f"  {name:<28} {c:>3}  {'#' * c}")

    by_ship = defaultdict(list)
    for r in reviews:
        by_ship[shipping(r["logistics"])].append(len(r["comment"] or ""))
    print("\nAverage comment length by shipping:")
    for name, lens in sorted(by_ship.items(), key=lambda kv: -len(kv[1])):
        print(f"  {name:<28} {sum(lens) / len(lens):>5.0f} chars  ({len(lens)} reviews)")
    kr = [r for r in reviews if r["country"] == "KR"]
    prem = [r for r in kr if "Premium" in r["logistics"]]
    print(f"\nKorea: {len(kr)} reviews, {len(prem)} with Premium shipping")


if __name__ == "__main__":
    pid = sys.argv[1] if len(sys.argv) > 1 else "3256807637171608"
    pages = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    report([call("/product/reviews", productId=pid, page=p, pageSize=20, filter="all") for p in range(1, pages + 1)])
