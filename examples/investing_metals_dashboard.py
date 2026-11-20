"""Metals dashboard: live futures prices and daily moves (Investing.com Ultimate API).

Usage:
    export RAPIDAPI_KEY=your_key
    python investing_metals_dashboard.py metals
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


def metals(group="metals"):
    body = call("/v2/markets/commodities", group=group)
    for block in body["data"]:
        print(f"\n== {block['table']} ==")
        for r in sorted(block["rows"], key=lambda x: x["change_percent"]):
            month = r.get("contract_month") or "-"
            print(f"{r['name']:<18}{r['last']:>12,.2f}{r['change_percent']:>8.2f}%  {month}")
    return body


if __name__ == "__main__":
    metals(sys.argv[1] if len(sys.argv) > 1 else "metals")
