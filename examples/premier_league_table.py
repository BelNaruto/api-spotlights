"""Premier League table with qualification and relegation zones. Uses the English Premier League API on RapidAPI."""
import os, sys, time
import requests

HOST = "english-premiere-league1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def league_table(season):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/tables", headers=HEADERS,
                         params={"season": season}, timeout=60)
        if r.ok:
            return r.json()["children"][0]["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def zone(position, size):
    if position == 1:
        return "CHAMPION"
    if position in (2, 3, 4):
        return "Champions League"
    if position == 5:
        return "Europa League"
    if position in range(size - 2, size + 1):
        return "Relegation"
    return ""


def main(season):
    entries = league_table(season)
    rows = []
    for e in entries:
        s = {x["name"]: x.get("value") for x in e["stats"]}
        rows.append((s["points"], s["pointDifferential"], s["pointsFor"], e["team"]["displayName"], s))
    rows.sort(reverse=True)
    print("#".rjust(2) + "  " + "Team".ljust(24) + "P".rjust(3) + "  W-D-L".ljust(10) + "GD".rjust(4) + "PTS".rjust(5) + "  PPG   Zone")
    for pos, (pts, gd, gf, team, s) in enumerate(rows, 1):
        record = f"{s['wins']:.0f}-{s['ties']:.0f}-{s['losses']:.0f}"
        ppg = pts / s["gamesPlayed"]
        print(f"{pos:2}  " + team.ljust(24) + f"{s['gamesPlayed']:3.0f}  " + record.ljust(8) +
              f"{gd:+4.0f}{pts:5.0f}  {ppg:.2f}  {zone(pos, len(rows))}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["2025"])[0])
