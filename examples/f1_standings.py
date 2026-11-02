"""F1 championship table with gap to the leader. Uses the F1 Motorsport Data API on RapidAPI."""
import os, sys, time
import requests

HOST = "f1-motorsport-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def driver_standings(year):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/standings-drivers", headers=HEADERS,
                         params={"year": year}, timeout=60)
        if r.ok:
            return r.json()["standings"]["entries"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year="2024", top=10):
    rows = []
    for e in driver_standings(year):
        stats = {s["name"]: s for s in e["stats"]}
        races = [s for s in e["stats"] if s.get("played")]
        best = max(races, key=lambda s: s["value"]) if races else None
        rows.append((stats["rank"]["value"], e["athlete"]["displayName"],
                     stats["championshipPts"]["value"], len(races), best))
    rows.sort()
    leader = rows[0][2]
    print(f"F1 {year} drivers championship")
    for rank, name, pts, n, best in rows[:int(top)]:
        gap = "leader" if pts == leader else f"-{leader - pts:g}"
        peak = f"best: {best['value']:g} pts at {best['shortName']}" if best else ""
        print(f"{int(rank):2d}. {name.ljust(20)} {pts:6g} pts  {gap.rjust(7)}  {peak}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
