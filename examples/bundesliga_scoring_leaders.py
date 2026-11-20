"""Print a Bundesliga team's scoring leaders and season totals (German Bundesliga API).

Usage:
    export RAPIDAPI_KEY=your_key
    python bundesliga_scoring_leaders.py 131 2025
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


def leaders(team_id, season):
    body = call("/team/statistic/scoring", teamId=team_id, season=season)
    stats = {s["name"]: s["leaders"] for s in body["results"]["stats"]}
    print(f"{body['team']['displayName']}, {body['requestedSeason']['displayName']}\n")
    for key, label in [("goals", "Goals"), ("assists", "Assists"), ("shotsOnTarget", "Shots on target"), ("totalShots", "Total shots"), ("saves", "Saves")]:
        top = ", ".join(f"{x['athlete']['displayName']} {x['value']}" for x in stats[key][:3])
        print(f"{label:<16}{top}")
    totals = {k: sum(x["value"] or 0 for x in stats[k]) for k in ["goals", "assists", "shotsOnTarget", "totalShots", "saves"]}
    print("\nTotals of the players listed:", totals)
    print(f"{len(stats['goals'])} players listed, {sum(not x['value'] for x in stats['goals'])} without a goal")
    return stats


if __name__ == "__main__":
    args = sys.argv[1:]
    leaders(args[0] if args else "131", args[1] if len(args) > 1 else "2025")
