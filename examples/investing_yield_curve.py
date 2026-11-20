"""US Treasury yield curve with spreads and inversion check (Investing.com Ultimate API).

Usage:
    export RAPIDAPI_KEY=your_key
    python investing_yield_curve.py US
"""
import os
import sys
import time

import requests

HOST = "investing-com-ultimate-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def curve(country="US"):
    body = call("/v2/markets/bonds", country=country)
    rows = {r["name"].split()[-1]: r for r in body["data"]}
    print(f"{body['meta']['country']['name']} government bond yields ({body['meta']['unit']})\n")
    print(f"{'Tenor':<6}{'Yield':>8}{'Prev':>8}{'Change':>8}")
    for tenor, r in rows.items():
        print(f"{tenor:<6}{r['yield']:>8.3f}{r['previous_close']:>8.3f}{r['change']:>8.3f}")
    spread = lambda a, b: (rows[a]["yield"] - rows[b]["yield"]) * 100
    print(f"\n10Y-2Y spread: {spread('10Y', '2Y'):+.1f} bp")
    print(f"10Y-3M spread: {spread('10Y', '3M'):+.1f} bp")
    print("Curve:", "INVERTED (10Y-2Y < 0)" if spread("10Y", "2Y") < 0 else "normal (10Y above 2Y)")
    return rows


if __name__ == "__main__":
    curve(sys.argv[1] if len(sys.argv) > 1 else "US")
