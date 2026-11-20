"""PGA Tour money list: earnings, FedExCup points, wins and driving distance.

Usage:
    export RAPIDAPI_KEY=your_key
    python golf_money_list.py 2026
"""
import os
import sys
import time

import requests

HOST = "live-golf-data1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}

# Position of each number in categories[0]["totals"]. The glossary in the response is sorted
# alphabetically and does not follow this order, so we read by position.
EARNINGS, FEDEX_POINTS, EVENTS, CUTS_MADE, TOP10, WINS, GREENS_PCT, DRIVE_YDS = 0, 1, 2, 4, 5, 6, 7, 8


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(season="2026", limit=10):
    athletes = call("/players-stats", league="pga", season=season, limit=limit)["players_stats"]["athletes"]
    print(f"PGA Tour {season} money list (top {limit})")
    print(f"{'#':<3}{'Player':<20}{'Earnings':>12}{'FedEx pts':>10}{'Events':>7}{'Cuts':>6}{'Top10':>6}{'Wins':>5}{'Drive':>7}{'GIR%':>6}")
    for i, a in enumerate(athletes, 1):
        t = a["categories"][0]["totals"]
        print(f"{i:<3}{a['athlete']['displayName']:<20}{t[EARNINGS]:>12}{t[FEDEX_POINTS]:>10}{t[EVENTS]:>7}"
              f"{t[CUTS_MADE]:>6}{t[TOP10]:>6}{t[WINS]:>5}{t[DRIVE_YDS]:>7}{t[GREENS_PCT]:>6}")

    best = max(athletes, key=lambda a: float(a["categories"][0]["totals"][DRIVE_YDS]))
    print(f"\nLongest driver in this top {limit}: {best['athlete']['displayName']} "
          f"({best['categories'][0]['totals'][DRIVE_YDS]} yards)")


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "2026")
