"""Compare resale prices for one sneaker across StockX, GOAT, Flight Club and Stadium Goods.

Uses the Sneaker Database - StockX API (RapidAPI). Each marketplace comes back in a
different shape, so the script first normalises them to {size: lowest new price}.

Usage:
    export RAPIDAPI_KEY=your_key
    python stockx_price_compare.py HQ6448
"""
import os
import sys
import time

import requests

HOST = "sneaker-database-stockx.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}
NAMES = {"stockX": "StockX", "goat": "GOAT", "flightClub": "Flight Club", "stadiumGoods": "Stadium Goods"}
SHORT = {"stockX": "SX", "goat": "GOAT", "flightClub": "FC", "stadiumGoods": "SG"}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def lowest_by_size(resell):
    """Return {marketplace: {size: lowest price for a new pair}}."""
    out = {}
    # StockX: {"4": 109, "5": 142, ...}
    out["stockX"] = {float(s): p for s, p in resell["stockX"].items() if p}
    # Stadium Goods: [{"size": "3", "price": 99}, ...]
    out["stadiumGoods"] = {float(x["size"]): x["price"] for x in resell["stadiumGoods"] if x.get("price")}
    # Flight Club: {"newSizes": [{"size": {"display": "4"}, "lowestPriceOption": {"price": 122}}, ...]}
    fc = {}
    for x in resell["flightClub"].get("newSizes", []):
        size, price = float(x["size"]["display"]), x["lowestPriceOption"]["price"]
        fc[size] = min(price, fc.get(size, price))
    out["flightClub"] = fc
    # GOAT: [{"size": 4, "lowestPrice": 71, "shoeCondition": "new_no_defects"}, ...]
    goat = {}
    for x in resell["goat"]:
        if x["shoeCondition"] == "new_no_defects" and x.get("lowestPrice"):
            goat[float(x["size"])] = min(x["lowestPrice"], goat.get(float(x["size"]), 10**9))
    out["goat"] = goat
    return out


def compare(style_id, data=None):
    d = data or call("/productprice", styleId=style_id)
    print(f"{d['shoeName']} ({d['styleID']}), retail ${d['retailPrice']}, released {d['releaseDate']}")
    print(f"StockX lowest ask ${d['lowestAsk']}, last sale ${d['lastSale']}\n")

    by_size = lowest_by_size(d["resellPrices"])
    print("Cheapest new pair per marketplace (computed from the size data):")
    for key, sizes in sorted(by_size.items(), key=lambda kv: min(kv[1].values())):
        size, price = min(sizes.items(), key=lambda kv: kv[1])
        print(f"  {NAMES[key]:<14} ${price:<5g} size {size:g}   ({len(sizes)} sizes listed)")

    print("\nWhat the lowestResellPrice block says:")
    for key, price in d["lowestResellPrice"].items():
        real = min(by_size[key].values())
        flag = "" if price == real else f"   <- size data says ${real:g}"
        print(f"  {NAMES[key]:<14} ${price}{flag}")

    print("\nBest marketplace per size:")
    wins = {k: 0 for k in by_size}
    for size in sorted(set().union(*[s.keys() for s in by_size.values()])):
        offers = {k: s[size] for k, s in by_size.items() if size in s}
        best = min(offers, key=offers.get)
        wins[best] += 1
        row = "  ".join(f"{SHORT[k]:<4} " + (f"${offers[k]:g}" if k in offers else "--").ljust(5) for k in by_size)
        print(f"  size {size:>4g}  {row}  -> {NAMES[best]}")
    print("\nSizes won: " + ", ".join(f"{NAMES[k]} {n}" for k, n in sorted(wins.items(), key=lambda kv: -kv[1])))
    return by_size


if __name__ == "__main__":
    compare(sys.argv[1] if len(sys.argv) > 1 else "HQ6448")
