"""Recap one Champions League matchday: scores, goals, cards and attendance (UEFA Champions League API).

Usage:
    export RAPIDAPI_KEY=your_key
    python uefa_matchday_recap.py 2026 01 28
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


def recap(year, month, day):
    events = call("/scoreboard", year=year, month=month, day=day)["scoreboard"]["events"]
    goals = yellow = red = pens = 0
    scorers = Counter()
    attendance = []
    print(f"{len(events)} matches on {year}-{month}-{day}\n")
    for e in events:
        c = e["competitions"][0]
        home = next(t for t in c["competitors"] if t["homeAway"] == "home")
        away = next(t for t in c["competitors"] if t["homeAway"] == "away")
        print(f"{home['team']['shortDisplayName']:<14}{home['score']:>2} - {away['score']:<2}{away['team']['shortDisplayName']:<14}"
              f"{c['status']['type']['description']:<10}{c.get('attendance', 0):>7,}")
        attendance.append(int(c.get("attendance") or 0))
        for d in c.get("details", []):
            yellow += bool(d.get("yellowCard"))
            red += bool(d.get("redCard"))
            if d.get("scoringPlay"):
                goals += 1
                pens += bool(d.get("penaltyKick"))
                if d.get("athletesInvolved") and not d.get("ownGoal"):
                    scorers[d["athletesInvolved"][0]["displayName"]] += 1
    print(f"\n{goals} goals ({goals / len(events):.2f} per match), {pens} penalties, {yellow} yellow cards, {red} red cards")
    print(f"Attendance: {sum(attendance):,} total, biggest {max(attendance):,}, smallest {min(attendance):,}")
    print("Players with 2+ goals:", [n for n, g in scorers.items() if g >= 2])
    return events


if __name__ == "__main__":
    args = sys.argv[1:] or ["2026", "01", "28"]
    recap(*args)
