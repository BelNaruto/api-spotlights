"""Rank the most popular sneakers on StockX by resale premium over retail price.

Uses the Sneaker Database - StockX API (RapidAPI), endpoint /mostpopular.

Usage:
    export RAPIDAPI_KEY=your_key
    python stockx_resale_premium.py 20
"""
import os
import sys
import time

import requests

HOST = "sneaker-database-stockx.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def analyse(shoes):
    rows = []
    for s in shoes:
        retail, ask, last = num(s.get("retailPrice")), num(s.get("lowestAsk")), num(s.get("lastSale"))
        markets = {k: v for k, v in (s.get("lowestResellPrice") or {}).items() if v}
        if not retail or not ask:
            continue
        rows.append({
            "name": s["shoeName"], "release": s["releaseDate"], "retail": retail, "ask": ask, "last": last,
            "premium": (ask / retail - 1) * 100, "markets": markets,
            "cheapest": min(markets, key=markets.get), "spread": max(markets.values()) / min(markets.values()),
        })
    return sorted(rows, key=lambda r: -r["premium"])


def report(shoes):
    rows = analyse(shoes)
    print(f"{len(shoes)} sneakers returned, {len(rows)} with a retail price and a StockX ask\n")
    print(f"{'Sneaker':<48}{'Retail':>7}{'Ask':>6}{'Prem.':>7}  Cheapest")
    for r in rows:
        print(f"{r['name'][:46]:<48}{r['retail']:>7g}{r['ask']:>6g}{r['premium']:>+6.0f}%  {r['cheapest']} ${r['markets'][r['cheapest']]:g}")
    above = [r for r in rows if r["premium"] > 0]
    below = [r for r in rows if r["premium"] < 0]
    print(f"\nAbove retail: {len(above)}   Below retail: {len(below)}   "
          f"Average premium: {sum(r['premium'] for r in rows) / len(rows):+.0f}%")
    print("\nBiggest gap between marketplaces (highest lowest-price / cheapest lowest-price):")
    for r in sorted(rows, key=lambda r: -r["spread"])[:3]:
        prices = ", ".join(f"{k} ${v:g}" for k, v in sorted(r["markets"].items(), key=lambda kv: kv[1]))
        print(f"  {r['name'][:46]:<48}x{r['spread']:.1f}  ({prices})")
    return rows


if __name__ == "__main__":
    limit = sys.argv[1] if len(sys.argv) > 1 else "20"
    report(call("/mostpopular", limit=limit))
