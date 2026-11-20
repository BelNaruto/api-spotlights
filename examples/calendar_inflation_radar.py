"""Inflation and central bank radar across several countries.

Usage:
    export RAPIDAPI_KEY=your_key
    python calendar_inflation_radar.py 23/11/2026 04/12/2026
"""
import os
import sys
import time
from collections import Counter

import requests

HOST = "trader-calendar-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def radar(from_date, to_date, countries="united states,euro zone,united kingdom,japan"):
    events = call("/calendar", from_date=from_date, to_date=to_date, importances="medium,high",
                  categories="inflation,central_banks", countries=countries)
    print(f"{len(events)} events, by country: {dict(Counter(e['zone'] for e in events))}\n")
    for e in events:
        if e["category"] == "inflation" and e["importance"] == "high":
            print(f"{e['date']} {e['time']} {e['zone']:<14} {e['event']:<38} prev={e['previous'] or '-'} fcst={e['forecast'] or '-'}")
    return events


if __name__ == "__main__":
    radar(sys.argv[1], sys.argv[2])
