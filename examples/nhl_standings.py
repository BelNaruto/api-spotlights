"""NHL standings table with points percentage. Uses the NHL API on RapidAPI."""
import os, sys, time
import requests

HOST = "nhl-api5.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/nhlstandings", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year, top):
    rows = []
    for e in standings(year):
        s = {x["name"]: x.get("value") for x in e["stats"]}
        gp, pts = s["gamesPlayed"], s["points"]
        rows.append((pts / (2 * gp), e["team"]["displayName"], gp, s["wins"], s["losses"],
                     s["otLosses"], pts, s["pointDifferential"]))
    rows.sort(reverse=True)
    print(f"{'#':>2}.  {'Team':<22} {'GP':>2}  W-L-OTL".ljust(40) + " PTS  PTS%   GD")
    for i, (pct, team, gp, w, l, otl, pts, gd) in enumerate(rows[:top], 1):
        print(f"{i:>2}.  {team:<22} {gp:>2.0f}  {w:.0f}-{l:.0f}-{otl:.0f}".ljust(40) + f"{pts:>4.0f}  {pct:5.3f}  {gd:+.0f}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "2025", int(sys.argv[2]) if len(sys.argv) > 2 else 10)
