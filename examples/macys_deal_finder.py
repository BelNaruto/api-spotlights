"""Macy's deal finder: search a product and rank results by discount.

Usage:
    export RAPIDAPI_KEY=your_key
    python macys_deal_finder.py "levi's 501 jeans" 10
"""
import os
import sys
import time

import requests

HOST = "macys4.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("status") != "success":
                raise RuntimeError(body)
            return body["result"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def deal_finder(query, per_page=10):
    result = call("/api/search/product", q=query, perPage=per_page)
    page = result["pagination"]
    print(f"{page['totalAvailable']} products match '{query}'. Showing {page['from']}-{page['to']}\n")
    rows = []
    for p in result["products"]:
        s = p["priceSummary"]
        rating = (p["detail"].get("reviewStatistics") or {}).get("aggregate") or {}
        rows.append((s.get("percentOff") or 0, p["detail"]["name"], s["current"], s["regular"], rating.get("rating"), rating.get("count")))
    for off, name, cur, reg, rating, n in sorted(rows, reverse=True):
        print(f"{off:>3}% off  ${cur:>7.2f}  (was ${reg:>6.2f})  {rating or '-'} ({n or 0})  {name[:52]}")
    return rows


if __name__ == "__main__":
    deal_finder(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)
