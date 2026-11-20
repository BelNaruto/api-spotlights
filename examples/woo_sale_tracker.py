"""Sale tracker for any WooCommerce store: biggest discounts first (WooCommerce Stores Hub API).

Usage:
    export RAPIDAPI_KEY=your_key
    python woo_sale_tracker.py dogoutfit.co.uk 10
"""
import os
import sys
import time

import requests

HOST = "woocommerce-stores-hub.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body)
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def sale_tracker(store, per_page=10):
    data = call("/product/on-sale", url=store, perPage=per_page)
    total = data["pagination"]["total"]
    print(f"{store}: {total} products on sale. Showing {len(data['products'])}\n")
    rows = []
    for p in data["products"]:
        pr = p["prices"]
        # Trust the prices, not the flag: some items come back with onSale=false.
        real_discount = round((1 - pr["price"] / pr["regularPrice"]) * 100) if pr.get("regularPrice") else 0
        rows.append((real_discount, pr["price"], pr["regularPrice"], pr["currency"], p["onSale"], p["name"]))
    for off, price, reg, cur, flag, name in sorted(rows, reverse=True):
        note = "" if flag else "  (flagged onSale=false)"
        print(f"{off:>3}% off  {price:>7.2f} {cur} (was {reg:>6.2f})  {name[:48]}{note}")
    return rows


if __name__ == "__main__":
    sale_tracker(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)
