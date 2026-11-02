"""WNBA injury report grouped by injury type. Uses the WNBA API on RapidAPI."""
import os, sys, time
from collections import defaultdict
import requests

HOST = "wnba-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def injuries():
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/injuries", headers=HEADERS, timeout=60)
        if r.ok:
            return r.json()["injuries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(top=5):
    by_type = defaultdict(list)
    for team in injuries():
        for item in team["injuries"]:
            by_type[item["details"]["type"]].append((item["athlete"]["displayName"], team["displayName"]))
    total = sum(len(v) for v in by_type.values())
    print(f"{total} players on the WNBA injury report\n")
    for kind, players in sorted(by_type.items(), key=lambda kv: len(kv[1]), reverse=True)[:int(top)]:
        print(f"{kind} ({len(players)})")
        for name, team in players[:3]:
            print(f"  {name.ljust(24)} {team}")


if __name__ == "__main__":
    main(*sys.argv[1:2])
