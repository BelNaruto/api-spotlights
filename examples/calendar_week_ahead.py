"""Week-ahead market calendar: high-impact events grouped by day.

Usage:
    export RAPIDAPI_KEY=your_key
    python calendar_week_ahead.py 23/11/2026 27/11/2026
"""
import os
import sys
import time
from collections import defaultdict

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


def week_ahead(from_date, to_date, importances="high", countries="united states,euro zone"):
    events = call("/calendar", from_date=from_date, to_date=to_date, importances=importances, countries=countries)
    by_day = defaultdict(list)
    for e in events:
        by_day[e["date"]].append(e)
    for day, items in by_day.items():
        print(f"\n{day}")
        for e in sorted(items, key=lambda x: x["time"]):
            print(f"  {e['time']}  {e['event']:<42} forecast={e['forecast'] or '-':<7} previous={e['previous'] or '-'}")
    return events


if __name__ == "__main__":
    week_ahead(sys.argv[1], sys.argv[2])
