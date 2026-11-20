"""Check which fashion retailers are live before you search (Fashion Product API).

Usage:
    export RAPIDAPI_KEY=your_key
    python fashion_retailer_coverage.py
"""
import os
import time
from collections import Counter

import requests

HOST = "fashion-product-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            if body.get("error"):
                raise RuntimeError(body["error"])
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def coverage():
    data = call("/retailers")
    print(f"{data['count']} retailers: {dict(Counter(r['status'] for r in data['retailers']))}\n")
    for r in sorted(data["retailers"], key=lambda r: (r["status"], r["label"])):
        print(f"{r['status']:<12}{r['label']:<18}{r['origin']}")
    return data


if __name__ == "__main__":
    coverage()
