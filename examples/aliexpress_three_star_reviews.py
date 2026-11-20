"""Read the 3-star reviews of an AliExpress product and see what buyers really say (AliExpress Data API).

Uses GET /product/reviews with filter=3, reads every page, and sorts each comment with a small
multilingual word list into: mentions a problem, positive, or neutral. A star rating is not always
the same as the text, so this shows how many 3-star reviews are real complaints.

Usage:
    export RAPIDAPI_KEY=your_key
    python aliexpress_three_star_reviews.py 3256807637171608
"""
import os
import sys
import time
from collections import Counter

import requests

HOST = "aliexpress-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}

# Starter lists: extend them with the languages your buyers write in.
PROBLEM = ["could be better", "melted", "looks cheap", "помят", "pequeña", "broken", "cracked", "loose", "yellow"]
NEUTRAL = ["ok", "ок", "норм", "pasan", "ca va", "لا باس به"]


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


def read_all(product_id, stars=3):
    pages, page = [], 1
    while True:
        data = call("/product/reviews", productId=product_id, filter=stars, page=page, pageSize=20)
        pages.append(data)
        if page >= data["pagination"]["totalPages"]:
            return pages
        page += 1


def classify(comment):
    text = (comment or "").lower().strip()
    if any(w in text for w in PROBLEM):
        return "problem"
    if text in NEUTRAL or any(text.startswith(w + " ") for w in NEUTRAL):
        return "neutral"
    return "positive"


def report(pages):
    reviews = [r for p in pages for r in p["reviews"]]
    pg = pages[0]["pagination"]
    print(f"filter=3 returned {len(reviews)} reviews on {pg['totalPages']} pages, but totalCount says {pg['totalCount']}")
    groups = {"problem": [], "neutral": [], "positive": []}
    for r in reviews:
        groups[classify(r["comment"])].append(r)
    for name, items in groups.items():
        print(f"  {name:<9} {len(items):>3}  ({len(items) / len(reviews):.0%})")
    print("\nReviews that mention a problem:")
    for r in groups["problem"]:
        sku = r["sku"].replace("Material:", "").replace("For iPhone", "").strip()
        print(f"  {r['country']}  iPhone {sku:<24} {r['comment'].strip()}")
    pro = sum(1 for r in groups["problem"] + groups["neutral"] if "Pro" in r["sku"])
    print(f"\nNon-positive reviews for a Pro model: {pro} of {len(groups['problem']) + len(groups['neutral'])}")
    top = ", ".join(f"{c} {n}" for c, n in Counter(r["country"] for r in reviews).most_common(5))
    print(f"Buyer countries in the 3-star group: {top}")


if __name__ == "__main__":
    report(read_all(sys.argv[1] if len(sys.argv) > 1 else "3256807637171608"))
