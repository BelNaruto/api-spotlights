"""Compare two to four trims side by side and flag which one wins each row (Car Specs API).

Usage:
    export RAPIDAPI_KEY=your_key
    python carspecs_compare.py 41189,47069
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


def compare(ids):
    data = call("/compare", ids=ids)
    vehicles = data["vehicles"]
    for v in vehicles:
        print(f"[{v['id']}] {v['summary']}")
    print()
    print(f"{'':<22}" + "".join(f"{v['name'][:22]:<24}" for v in vehicles))
    for row, info in data["comparison"].items():
        cells = []
        for v, value in zip(vehicles, info["values"]):
            mark = " *" if info.get("bestId") == v["id"] else ""
            cells.append(f"{str(value) + mark:<24}")
        print(f"{row:<22}" + "".join(cells))
    powertrains = set(data["comparison"]["powertrain"]["values"])
    if len(powertrains) > 1:
        print("\n* = best value. The powertrains differ, so MPGe (electric) is compared with MPG (fuel).")
    return data


if __name__ == "__main__":
    compare(sys.argv[1] if len(sys.argv) > 1 else "41189,47069")
