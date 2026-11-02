"""Premier League results for a month: biggest wins and goal stats. Uses the English Premier League API on RapidAPI."""
import os, sys, time
import requests

HOST = "english-premiere-league1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def matches(year, month):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/scoreboard", headers=HEADERS, timeout=60,
                         params={"year": year, "month": month, "limit": 100})
        if r.ok:
            return r.json()["scoreboard"]["events"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(year, month, top=5):
    results = []
    for event in matches(year, month):
        sides = {c["homeAway"]: c for c in event["competitions"][0]["competitors"]}
        home, away = sides["home"], sides["away"]
        results.append((event["date"][:10], home["team"]["displayName"], int(home["score"]),
                        away["team"]["displayName"], int(away["score"])))
    goals = sum(h + a for _, _, h, _, a in results)
    home_wins = sum(1 for _, _, h, _, a in results if h > a)
    away_wins = sum(1 for _, _, h, _, a in results if a > h)
    draws = len(results) - home_wins - away_wins
    print(f"{len(results)} matches, {goals} goals ({goals / len(results):.2f} per match)")
    print(f"home wins {home_wins}, draws {draws}, away wins {away_wins}\n")
    print("Biggest margins:")
    for date, home, h, away, a in sorted(results, key=lambda r: abs(r[2] - r[4]), reverse=True)[:int(top)]:
        print(f"  {date}  {home} {h}-{a} {away}")


if __name__ == "__main__":
    a = sys.argv[1:] + ["2026", "10"][len(sys.argv) - 1:]
    main(a[0], a[1])
