"""SHEIN price-drop tracker built on the Shein Data API (RapidAPI).

Usage:
    export RAPIDAPI_KEY=your_key
    python shein_price_tracker.py "summer dress"     # first run: saves a baseline
    python shein_price_tracker.py "summer dress"     # later runs: report price drops
"""
import json
import os
import sys
import time

import requests

HOST = "shein-data-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}
STATE_FILE = "prices.json"


def call(path, **params):
    """GET an endpoint, retry temporary upstream errors, return the `data` payload."""
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        body = r.json()
        if body.get("success"):
            return body["data"]
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(int(r.headers.get("Retry-After", 5)))
            continue
        raise RuntimeError(f"{body['error']['code']}: {body['error']['message']}")


def search(query, limit=20):
    data = call("/search/products", query=query, country="US", limit=limit, sort="popular")
    return {p["goods_id"]: p["name"] for p in data["products"]}


def current_prices(goods_ids):
    prices = {}
    for i in range(0, len(goods_ids), 10):  # the batch endpoint takes up to 10 ids
        data = call("/product/price/batch", goods_ids=",".join(goods_ids[i:i + 10]))
        for item in data["results"]:
            if item["ok"]:
                prices[item["goods_id"]] = item["data"]["price"]["sale"]["amount"]
    return prices


def main(query):
    names = search(query)
    now = current_prices(list(names))
    try:
        with open(STATE_FILE) as f:
            before = json.load(f)
    except FileNotFoundError:
        before = {}

    for goods_id, price in now.items():
        old = before.get(goods_id)
        if old is not None and price != old and price == min(price, old):
            print(f"DROP  ${old:.2f} to ${price:.2f}  {names[goods_id]}")

    before.update(now)
    with open(STATE_FILE, "w") as f:
        json.dump(before, f)
    print(f"Tracked {len(now)} products for '{query}'.")


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "summer dress")
