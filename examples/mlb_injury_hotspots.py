import os
import time
from collections import Counter

import requests

HOST = "major-league-baseball-mlb.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}


def injuries():
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/injuries", headers=HEADERS, timeout=60)
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()["injuries"]


def main(top=5):
    teams = injuries()
    by_type, by_team, pitchers, total = Counter(), Counter(), 0, 0
    for team in teams:
        for item in team["injuries"]:
            total += 1
            by_type[item["details"]["type"]] += 1
            by_team[team["displayName"]] += 1
            if item["athlete"]["position"]["abbreviation"] in ("SP", "RP"):
                pitchers += 1
    print(f"{total} players on the MLB injury report across {len(teams)} teams")
    print(f"Pitchers: {pitchers} ({round(100 * pitchers / total)}%)")
    print("\nMost common injuries")
    for kind, n in by_type.most_common(top):
        print(f"  {kind.ljust(12)} {n}")
    print("\nTeams with the most players listed")
    for name, n in by_team.most_common(top):
        print(f"  {name.ljust(24)} {n}")


if __name__ == "__main__":
    main()
