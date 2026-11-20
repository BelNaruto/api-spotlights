"""Find the cheapest country storefront for a sneaker, converted to one currency.

Usage:
    export RAPIDAPI_KEY=your_key
    python kickscrew_regional_price.py gs-air-jordan-11-retro-gamma-blue-2025-378038-047
"""
import os
import sys
import time

import requests

HOST = "kickscrew-sneakers-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("error"):
                raise RuntimeError(body["error"])
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def regional(handle, base="USD", countries="US,GB,CA,AU,DE,FR,JP,KR,SG,HK"):
    d = call(f"/v2/products/{handle}/regional-pricing", baseCurrency=base, countries=countries)
    print(f"{d['handle']}\nFX rates as of {d['fxRatesAsOf']}\n")
    for p in d["prices"]:
        extra = p["usdEquivalent"] - d["prices"][0]["usdEquivalent"]
        print(f"{p['country']:<4}{p['amount']:>10} {p['currency']:<4} = {p['usdEquivalent']:>7.2f} {base}  (+{extra:.2f})")
    print(f"\nCheapest: {d['cheapestCountry']}  Priciest: {d['priciestCountry']}  Max savings: {d['maxSavingsPercent']}%")
    return d


if __name__ == "__main__":
    regional(sys.argv[1])
