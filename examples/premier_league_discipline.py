"""Compare the discipline record of Premier League teams (English Premiere League API).

Usage:
    export RAPIDAPI_KEY=your_key
    python premier_league_discipline.py 2025 364 359 382
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


def stat(player, name):
    for s in player.get("statistics") or []:
        if s["name"] == name:
            return s["value"]
    return 0


def discipline(season, team_ids):
    print(f"{'Team':<18}{'Players':>8}{'Yellow':>8}{'Red':>5}{'Points':>8}   Most booked")
    for team_id in team_ids:
        body = call("/team/statistic/discipline", teamId=team_id, season=season)
        players = body["results"]
        yellow = sum(stat(p, "yellowCards") for p in players)
        red = sum(stat(p, "redCards") for p in players)
        points = sum(stat(p, "points") for p in players)
        worst = max(players, key=lambda p: (stat(p, "points"), stat(p, "yellowCards")))
        print(f"{body['team']['displayName']:<18}{len(players):>8}{yellow:>8}{red:>5}{points:>8}   "
              f"{worst['shortName']} ({stat(worst, 'yellowCards')} yellow, {stat(worst, 'redCards')} red)")


if __name__ == "__main__":
    args = sys.argv[1:]
    discipline(args[0] if args else "2025", args[1:] or ["364", "359", "382"])
