"""Rank every trim of a car model by fuel economy and running cost (Car Specs API).

Usage:
    export RAPIDAPI_KEY=your_key
    python carspecs_mpg_ladder.py honda civic 2024
"""
import os
import sys
import time

import requests

HOST = "car-specs-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("error"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def ladder(make, model, year):
    data = call("/mpg", make=make, model=model, year=year)
    v, rng = data["vehicle"], data["range"]
    trims = sorted(data["trims"], key=lambda t: -t["mpg"]["combined"])
    print(f"{v['year']} {v['make']} {v['model']}: {len(trims)} trims, combined {rng['combinedMin']} to {rng['combinedMax']} MPG\n")
    print(f"{'Id':>6}  {'Trim':<14}{'Engine':<20}{'Gearbox':<14}{'City':>5}{'Hwy':>5}{'Comb':>5}{'CO2 g/mi':>9}{'Fuel $/yr':>10}")
    for t in trims:
        print(f"{t['id']:>6}  {t['name'][5:].replace('Honda ', '')[:13]:<14}{t['engine']:<20}{t['transmission'][:13]:<14}"
              f"{t['mpg']['city']:>5}{t['mpg']['highway']:>5}{t['mpg']['combined']:>5}{t['co2GramsPerMile']:>9}{t['annualFuelCostUsd']:>10,}")
    best, worst = trims[0], trims[-1]
    print(f"\nBest vs worst: {best['annualFuelCostUsd']:,} vs {worst['annualFuelCostUsd']:,} USD a year "
          f"({worst['annualFuelCostUsd'] - best['annualFuelCostUsd']:,} difference)")
    return trims


if __name__ == "__main__":
    args = sys.argv[1:]
    ladder(*(args if len(args) == 3 else ["honda", "civic", "2024"]))
