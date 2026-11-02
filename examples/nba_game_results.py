"""NBA game results with quarter scores. Uses the Basketball API (NBA) on RapidAPI."""
import os, sys, time
import requests

HOST = "api-basketball-nba.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def scoreboard(year, month, day):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/nbascoreboard", headers=HEADERS, timeout=60,
                         params={"year": year, "month": month, "day": day, "limit": 20})
        if r.ok:
            return r.json()["events"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year, month, day):
    games = scoreboard(year, month, day)
    print(f"{len(games)} games on {year}-{month}-{day}\n")
    for game in games:
        comp = game["competitions"][0]["competitors"]
        print(f"{game['shortName']}  ({game['status']['type']['shortDetail']})")
        for team in sorted(comp, key=lambda c: c["homeAway"], reverse=True):
            quarters = "  ".join(q["displayValue"].rjust(2) for q in team["linescores"])
            mark = "W" if team["winner"] else " "
            print(f"  {mark} {team['team']['displayName'].ljust(24)} {quarters}  = {team['score'].rjust(3)}")


if __name__ == "__main__":
    main(*(sys.argv[1:] + ["2026", "11", "01"][len(sys.argv) - 1:]))
