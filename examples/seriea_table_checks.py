"""Check the Serie A table for data problems (Serie A API on RapidAPI).

Reads GET /tables?season=2025 and tests the numbers: points = 3 x wins + draws, wins + draws + losses
= games played, goals scored = goals conceded across the league, and the fields that come back empty.

Usage:
    export RAPIDAPI_KEY=your_key
    python seriea_table_checks.py 2025
"""
import sys

from seriea_table_report import call, rows


def check(data):
    season, table = rows(data)
    print(f"{season}: {len(table)} teams\n")
    problems = 0
    for s in table:
        if s["points"] != 3 * s["wins"] + s["ties"] - s["deductions"]:
            problems += 1
            print(f"  points mismatch: {s['team']} {int(s['points'])} vs {int(3 * s['wins'] + s['ties'])}")
        if s["wins"] + s["ties"] + s["losses"] != s["gamesPlayed"]:
            problems += 1
            print(f"  games mismatch: {s['team']}")
    gf, ga = sum(s["pointsFor"] for s in table), sum(s["pointsAgainst"] for s in table)
    print(f"Teams with wrong points or games: {problems}")
    print(f"Goals scored {int(gf)}, conceded {int(ga)} -> {'equal' if gf == ga else 'NOT equal'}")
    print(f"Games per team: {sorted({int(s['gamesPlayed']) for s in table})}")
    print(f"Teams with ppg = 0 in the API: {sum(1 for s in table if s['ppg'] == 0)} of {len(table)}")
    print(f"Teams with a deduction: {sum(1 for s in table if s['deductions'])}")
    zones = {}
    for s in table:
        zones[s["note"] or "(none)"] = zones.get(s["note"] or "(none)", 0) + 1
    print("Zones:", zones)


if __name__ == "__main__":
    check(call("/tables", season=sys.argv[1] if len(sys.argv) > 1 else "2025"))
