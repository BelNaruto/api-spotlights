"""NBA injury report by team. Uses the Basketball API (NBA) on RapidAPI."""
import os, sys, time
import requests

HOST = "api-basketball-nba.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def injuries():
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/nba-injuries", headers=HEADERS, timeout=60)
        if r.ok:
            return r.json()["injuries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(teams):
    data = injuries()
    data.sort(key=lambda t: len(t["injuries"]), reverse=True)
    total = sum(len(t["injuries"]) for t in data)
    print(f"{total} players on the injury report across {len(data)} teams\n")
    for team in data:
        name = team["displayName"]
        if teams and not any(t.lower() in name.lower() for t in teams):
            continue
        if not team["injuries"]:
            continue
        print(f"{name} ({len(team['injuries'])})")
        for item in team["injuries"]:
            player = item["athlete"]
            back = item.get("details", {}).get("returnDate", "unknown")
            print(f"  {player['displayName'].ljust(24)} {player['position']['abbreviation'].ljust(3)} "
                  f"{item['status'].ljust(12)} back: {back}")


if __name__ == "__main__":
    main(sys.argv[1:])
