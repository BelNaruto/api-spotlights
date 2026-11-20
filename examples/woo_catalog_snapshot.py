"""Catalog snapshot of a WooCommerce store: size, price range and category mix (WooCommerce Stores Hub API).

Usage:
    export RAPIDAPI_KEY=your_key
    python woo_catalog_snapshot.py dogoutfit.co.uk
"""
import os
import sys
import time
import statistics
from collections import Counter

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


def snapshot(store):
    data = call("/product/newest", url=store, perPage=20)
    products = data["products"]
    prices = sorted(p["prices"]["price"] for p in products)
    cats = Counter(c["name"] if isinstance(c, dict) else c for p in products for c in p.get("categories", []))
    print(f"{store}: {data['pagination']['total']} products in the catalog\n")
    print(f"Newest {len(products)} products")
    print(f"  currency : {products[0]['prices']['currency']}")
    print(f"  price    : min {prices[0]:.2f}, median {statistics.median(prices):.2f}, max {prices[-1]:.2f}")
    print(f"  on sale  : {sum(p['onSale'] for p in products)} of {len(products)}")
    print(f"  in stock : {sum(p['stock']['inStock'] for p in products)} of {len(products)}")
    print("  categories:", dict(cats.most_common()))
    return data


if __name__ == "__main__":
    snapshot(sys.argv[1])
