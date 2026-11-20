"""Compare the official ATP ranking with the API's Elo ratings.

Usage:
    export RAPIDAPI_KEY=your_key
    python tennis_elo_vs_ranking.py hard
"""
import os
import sys
import time

import requests

HOST = "tennis-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    """GET an endpoint and return the `data` part of the envelope (retries 5xx)."""
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(surface="hard", top=10):
    elo = call("/predictions/ratings", surface=surface, limit=top)["ratings"]
    atp = {r["player"]["id"]: r for r in call("/rankings", limit=100)["rankings"]}

    print(f"Top {top} by Elo on {surface} courts vs the official ATP ranking")
    print(f"{'Elo#':<5}{'Player':<30}{'Elo':>5}  {'ATP#':>5}{'Points':>8}")
    for e in elo:
        r = atp.get(e["id"])
        rank = f"{r['rank']}" if r else ">100"
        points = f"{r['points']}" if r else "-"
        print(f"{e['rank']:<5}{e['name']:<30}{e['rating']:>5}  {rank:>5}{points:>8}")

    movers = call("/rankings/movers", limit=3, top=100)
    print("\nBiggest risers in the latest ranking week")
    for m in movers["risers"]:
        print(f"  +{m['movement']}  #{m['rank']}  {m['player']['name']} ({m['player']['countryCode']})")
    print("Biggest fallers")
    for m in movers["fallers"]:
        print(f"  {m['movement']}  #{m['rank']}  {m['player']['name']} ({m['player']['countryCode']})")


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "hard")
