"""Print a team's scoring leaders and season totals (English Premiere League API).

Usage:
    export RAPIDAPI_KEY=your_key
    python premier_league_scoring_leaders.py 364 2025
"""
import os
import sys
import time

import requests

HOST = "english-premiere-league1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("status") != "success":
                raise RuntimeError(body)
            return body
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def leaders(team_id, season):
    body = call("/team/statistic/scoring", teamId=team_id, season=season)
    stats = {s["name"]: s["leaders"] for s in body["results"]["stats"]}
    print(f"{body['team']['displayName']}, {body['requestedSeason']['displayName']}\n")
    for key, label in [("goals", "Goals"), ("assists", "Assists"), ("shotsOnTarget", "Shots on target"), ("totalShots", "Total shots")]:
        top = ", ".join(f"{x['athlete']['displayName']} {x['value']}" for x in stats[key][:3])
        print(f"{label:<16}{top}")
    print("\nTeam totals (sum of the players listed):")
    for key in ["goals", "assists", "shotsOnTarget", "totalShots", "saves"]:
        print(f"  {key:<14}{sum(x['value'] or 0 for x in stats[key]):>6}")
    print(f"  players listed {len(stats['goals']):>6}, without a goal {sum(not x['value'] for x in stats['goals'])}")
    return stats


if __name__ == "__main__":
    args = sys.argv[1:]
    leaders(args[0] if args else "364", args[1] if len(args) > 1 else "2025")
