"""Serie A final table with points per game and goal difference (Serie A API on RapidAPI).

The table is returned by GET /tables?season=2025 (season 2025 = 2025-26). Each entry has a team and a
list of `stats`. The API sends `ppg` as 0, so the script calculates points per game itself.

Usage:
    export RAPIDAPI_KEY=your_key
    python seriea_table_report.py 2025
"""
import os
import sys
import time

import requests

HOST = "serie-a-api1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("message"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def rows(data):
    st = data["children"][0]["standings"]
    out = []
    for e in st["entries"]:
        s = {x["name"]: x["value"] for x in e["stats"]}
        s["team"] = e["team"]["displayName"]
        s["note"] = (e.get("note") or {}).get("description", "")
        out.append(s)
    return st["seasonDisplayName"], sorted(out, key=lambda s: s["rank"])


def report(data):
    season, table = rows(data)
    print(season)
    print(f"{'#':>2} {'team':<16}{'P':>3}{'W':>4}{'D':>3}{'L':>3}{'GF':>4}{'GA':>4}{'GD':>5}{'pts':>5}{'ppg':>6}  zone")
    for s in table:
        gd = int(s["pointsFor"] - s["pointsAgainst"])
        ppg = s["points"] / s["gamesPlayed"]
        print(f"{int(s['rank']):>2} {s['team']:<16}{int(s['gamesPlayed']):>3}{int(s['wins']):>4}{int(s['ties']):>3}"
              f"{int(s['losses']):>3}{int(s['pointsFor']):>4}{int(s['pointsAgainst']):>4}{gd:>+5}{int(s['points']):>5}{ppg:>6.2f}  {s['note']}")
    best = max(table, key=lambda s: s["pointsFor"] - s["pointsAgainst"])
    print(f"\nBest goal difference: {best['team']} ({int(best['pointsFor'] - best['pointsAgainst']):+d})")


if __name__ == "__main__":
    report(call("/tables", season=sys.argv[1] if len(sys.argv) > 1 else "2025"))
