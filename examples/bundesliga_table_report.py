"""Print the Bundesliga table with goals, European places and relegation (German Bundesliga API).

Usage:
    export RAPIDAPI_KEY=your_key
    python bundesliga_table_report.py 2025
"""
import os
import sys
import time

import requests

HOST = "german-bundesliga-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def table(year):
    league = call("/standings", year=year)["standings"]
    season = league["children"][0]
    entries = season["standings"]["entries"]
    print(f"{season['name']}\n")
    print(f"{'#':>2} {'Team':<26}{'P':>3}{'W':>4}{'D':>3}{'L':>3}{'GF':>5}{'GA':>5}{'GD':>5}{'Pts':>5}  Note")
    goals = 0
    for e in entries:
        s = {x["name"]: x.get("value") for x in e["stats"]}
        goals += s["pointsFor"]
        assert 3 * s["wins"] + s["ties"] - (s.get("deductions") or 0) == s["points"], e["team"]["displayName"]
        note = e["note"]["description"] if e.get("note") else ""
        print(f"{int(s['rank']):>2} {e['team']['displayName']:<26}{int(s['gamesPlayed']):>3}{int(s['wins']):>4}{int(s['ties']):>3}"
              f"{int(s['losses']):>3}{int(s['pointsFor']):>5}{int(s['pointsAgainst']):>5}{int(s['pointDifferential']):>5}{int(s['points']):>5}  {note}")
    games = len(entries) * int(s["gamesPlayed"]) // 2
    print(f"\n{goals} goals in {games} matches, {goals / games:.2f} per match")
    return entries


if __name__ == "__main__":
    table(sys.argv[1] if len(sys.argv) > 1 else "2025")
