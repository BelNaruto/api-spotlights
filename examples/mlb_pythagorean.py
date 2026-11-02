"""MLB standings with Pythagorean expectation. Uses the MLB API on RapidAPI."""
import os, sys, time
import requests

HOST = "major-league-baseball-mlb.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/standings", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def pythagorean(runs_scored, runs_allowed):
    """Expected win percentage from runs scored and allowed (exponent 1.83)."""
    rs, ra = runs_scored ** 1.83, runs_allowed ** 1.83
    return rs / (rs + ra)


def main(year):
    rows = []
    for e in standings(year):
        s = {x["name"]: x.get("value") for x in e["stats"]}
        games = s["wins"] + s["losses"]
        expected = pythagorean(s["pointsFor"], s["pointsAgainst"]) * games
        rows.append((s["winPercent"], e["team"]["displayName"], s["wins"], s["losses"],
                     s["pointsFor"], s["pointsAgainst"], s["wins"] - expected))
    rows.sort(reverse=True)
    print("Team".ljust(24) + "W-L".ljust(9) + "RS".ljust(6) + "RA".ljust(6) + "RUN DIFF".ljust(10) + "WINS VS EXPECTED")
    for pct, team, w, l, rs, ra, luck in rows:
        print(team.ljust(24) + f"{w:.0f}-{l:.0f}".ljust(9) + f"{rs:.0f}".ljust(6) +
              f"{ra:.0f}".ljust(6) + f"{rs - ra:+.0f}".ljust(10) + f"{luck:+.1f}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["2025"])[0])
