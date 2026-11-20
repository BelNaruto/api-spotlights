"""Macy's Black Friday deals: biggest savings in dollars and percent.

Usage:
    export RAPIDAPI_KEY=your_key
    python macys_black_friday_deals.py 10
"""
import html
import os
import sys
import time

import requests

HOST = "macys4.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            if body.get("status") != "success":
                raise RuntimeError(body)
            return body["result"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def deals(per_page=10):
    result = call("/api/deals/products", page=1, perPage=per_page)
    print(f"{result['pagination']['totalAvailable']} deal products available\n")
    rows = []
    for p in result["products"]:
        s = p["priceSummary"]
        rows.append((s["regular"] - s["current"], s.get("percentOff"), html.unescape(p["detail"]["brand"]),
                     html.unescape(p["detail"]["name"]), s["current"], s["regular"], s.get("promotion")))
    for saved, off, brand, name, cur, reg, promo in sorted(rows, reverse=True):
        print(f"save ${saved:>6.2f} ({off}%)  ${cur:>7.2f} was ${reg:>6.2f}  [{promo}]  {brand}: {name[:44]}")
    return rows


if __name__ == "__main__":
    deals(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
