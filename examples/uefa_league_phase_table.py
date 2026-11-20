"""Print the Champions League league-phase table with qualification zones (UEFA Champions League API).

Usage:
    export RAPIDAPI_KEY=your_key
    python uefa_league_phase_table.py 2025
"""
import os
import sys
import time
from collections import Counter

import requests

HOST = "uefa-champions-league1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def stat(entry, name):
    for s in entry["stats"]:
        if s["name"] == name:
            return s["displayValue"]
    return "?"


def table(season):
    data = call("/standingsv2", season=season)
    standings = data["children"][0]["standings"]
    entries = standings["entries"]
    print(f"{standings['seasonDisplayName']}: {len(entries)} teams\n")
    print(f"{'#':>2} {'Team':<22}{'P':>3}{'W':>3}{'D':>3}{'L':>3}{'GD':>5}{'Pts':>4}  Zone")
    zones = Counter()
    goals = played = 0
    for e in entries:
        zone = (e.get("note") or {}).get("description", "-")
        zones[zone] += 1
        goals += int(stat(e, "pointsFor"))
        played += int(stat(e, "gamesPlayed"))
        print(f"{stat(e, 'rank'):>2} {e['team']['displayName']:<22}{stat(e, 'gamesPlayed'):>3}"
              f"{stat(e, 'wins'):>3}{stat(e, 'ties'):>3}{stat(e, 'losses'):>3}"
              f"{stat(e, 'pointDifferential'):>5}{stat(e, 'points'):>4}  {zone}")
    matches = played // 2
    print(f"\n{matches} matches, {goals} goals ({goals / matches:.2f} per match)")
    print(dict(zones))
    return entries


if __name__ == "__main__":
    table(sys.argv[1] if len(sys.argv) > 1 else "2025")
