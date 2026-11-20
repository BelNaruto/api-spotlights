"""How much insider selling happens under a Rule 10b5-1 plan? (SEC Filings API on RapidAPI).

Reads GET /v1/insiders/{ticker}/trades (Form 4). For every open-market sale (code S) the script
checks the footnotes for a "10b5-1" trading plan and totals the value per insider.

Usage:
    export RAPIDAPI_KEY=your_key
    python sec_insider_10b5.py AAPL 10
"""
import os
import sys
import time
from collections import defaultdict

import requests

HOST = "sec-filings-api2.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("error"):
                raise RuntimeError(body.get("message"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def sales(trades):
    """Yield one row per open-market sale line: (date, insider, shares, price, under_plan)."""
    for t in trades:
        owner = t["reportingOwners"][0]["name"]
        for x in t.get("nonDerivativeTransactions", []):
            if x["transactionCode"] != "S":
                continue
            plan = any("10b5-1" in f for f in x.get("footnotes") or [])
            yield t["filingDate"], owner, x["shares"], x["pricePerShare"], plan


def report(trades):
    rows = list(sales(trades))
    by = defaultdict(lambda: {"n": 0, "shares": 0, "usd": 0.0, "plan": 0})
    for _, owner, shares, price, plan in rows:
        b = by[owner]
        b["n"] += 1
        b["shares"] += shares
        b["usd"] += shares * price
        b["plan"] += plan
    total = sum(b["usd"] for b in by.values())
    planned = sum(shares * price for _, _, shares, price, plan in rows if plan)
    print(f"{len(trades)} Form 4 filings, {len(rows)} open-market sale lines\n")
    print(f"{'insider':<22}{'sales':>6}{'shares':>9}{'USD':>12}{'under plan':>12}")
    for owner, b in sorted(by.items(), key=lambda kv: -kv[1]["usd"]):
        print(f"{owner[:21]:<22}{b['n']:>6}{b['shares']:>9,}{b['usd']:>12,.0f}{b['plan']:>9}/{b['n']}")
    print(f"\nTotal sold: ${total:,.0f}; ${planned:,.0f} ({planned / total * 100:.0f}%) was sold under a 10b5-1 plan")
    unplanned = [r for r in rows if not r[4]]
    for d, owner, shares, price, _ in unplanned:
        print(f"No plan footnote: {d} {owner} sold {shares:,} at ${price:,.2f}")


if __name__ == "__main__":
    ticker = (sys.argv[1] if len(sys.argv) > 1 else "AAPL").upper()
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    report(call(f"/v1/insiders/{ticker}/trades", limit=limit, form="4", since="2025-01-01")["trades"])
