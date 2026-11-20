"""Check the sport tags in a Decathlon collection (Decathlon API on RapidAPI).

Every product has tags such as `SPORT: mountain trekking`. The script lists products by sport, flags
products without a sport tag and bags whose sport looks wrong for their type.

Usage:
    export RAPIDAPI_KEY=your_key
    python decathlon_sport_tags.py new-arrivals
"""
import sys
from collections import Counter

from decathlon_discount_report import call

# Types where a sport tag such as "5-a-side Touch Rugby" or "aerial yoga" makes little sense.
BAGS = {"Backpack", "Sport bag", "Water bag"}


def sport(p):
    for tag in p["tags"]:
        if tag.startswith("SPORT: "):
            return tag[7:]
    return None


def report(products):
    sports = Counter((sport(p) or "(no sport tag)").lower() for p in products)
    print(f"{len(products)} products, {len(sports)} distinct sport values")
    for name, n in sports.most_common(6):
        print(f"  {n:>2}  {name}")
    missing = [p for p in products if not sport(p)]
    print(f"\nWithout a SPORT tag: {len(missing)}")
    for p in missing:
        print(f"  {p['product_type']:<10} {p['title']}")
    odd = [p for p in products if p["product_type"] in BAGS and sport(p) and sport(p).lower() not in
           ("hiking", "nature hiking", "mountain trekking", "all sports")]
    print(f"\nBags tagged with an unrelated sport: {len(odd)}")
    for p in odd:
        print(f"  {p['title']}  ->  {sport(p)}")

if __name__ == "__main__":
    report(call("/collection/products", collectionsHandle=sys.argv[1] if len(sys.argv) > 1 else "new-arrivals", page=1, country="us"))
