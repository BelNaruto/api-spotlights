"""WNBA standings with scoring margins. Uses the WNBA API on RapidAPI."""
import os, sys, time
import requests

HOST = "wnba-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/wnbastandings", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year):
    rows = []
    for e in standings(year):
        s = {x["name"]: x.get("value") for x in e["stats"]}
        margin = s["avgPointsFor"] - s["avgPointsAgainst"]
        rows.append((s["winPercent"], e["team"]["displayName"], s["wins"], s["losses"],
                     s["avgPointsFor"], s["avgPointsAgainst"], margin))
    rows.sort(reverse=True)
    print("Team".ljust(24) + "W-L".ljust(8) + "WIN%".ljust(7) + "PF".ljust(7) + "PA".ljust(7) + "MARGIN")
    for pct, team, w, l, pf, pa, margin in rows:
        record = f"{w:.0f}-{l:.0f}"
        print(team.ljust(24) + record.ljust(8) + f"{pct:.3f}".ljust(7) +
              f"{pf:.1f}".ljust(7) + f"{pa:.1f}".ljust(7) + f"{margin:+.1f}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["2025"])[0])
