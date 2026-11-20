"""Find discounted IKEA products for any search, ranked by discount (IKEA Data API).

Usage:
    export RAPIDAPI_KEY=your_key
    python ikea_deal_finder.py table
"""
import os
import sys
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


def money(p):
    return float(f"{p['wholeNumber']}.{p['decimals']}")


def deals(query):
    data = call("/search", query=query, type="normal", perPage=24)
    products = data["items"]["products"]  # "items" is an object: products, planner, content...
    sale = [p for p in products if p["salesPrice"].get("previous")]
    sale.sort(key=lambda p: -p["salesPrice"]["discountPercentage"])
    print(f"'{query}': {data['pagination']['totalAvailable']} results, {len(products)} products on this page, {len(sale)} discounted\n")
    print(f"{'Product':<28}{'Type':<20}{'Now':>9}{'Was':>9}{'Off':>6}  Valid until")
    for p in sale:
        s = p["salesPrice"]
        print(f"{p['name']:<28}{p['typeName'][:19]:<20}{s['numeral']:>9.2f}{money(s['previous']):>9.2f}{s['discountPercentage']:>5}%  {s['validTo']}")
    if sale:
        avg = sum(p["salesPrice"]["discountPercentage"] for p in sale) / len(sale)
        print(f"\nAverage discount {avg:.1f}%. Offer label: {sale[0]['salesPrice'].get('tagText')}")
    return sale


if __name__ == "__main__":
    deals(sys.argv[1] if len(sys.argv) > 1 else "table")
