"""PGA Tour season recap and the leaderboard of the latest completed event.

Usage:
    export RAPIDAPI_KEY=your_key
    python golf_event_recap.py 2026
"""
import os
import re
import sys
import time

import requests

HOST = "live-golf-data1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    """GET an endpoint and return the parsed JSON (retries temporary errors)."""
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def event_id(event):
    """The tournament id is the number at the end of the leaderboard link."""
    return re.search(r"tournamentId=(\d+)", event["link"]).group(1)


def season_recap(season):
    events = call("/schedule", season=season, league="pga")["events"]
    done = [e for e in events if e["status"] == "post" and not e["isPostponedOrCanceled"]]
    live = [e for e in events if e["status"] == "in"]
    upcoming = [e for e in events if e["status"] == "pre"]
    canceled = [e for e in events if e["isPostponedOrCanceled"]]
    print(f"PGA Tour {season}: {len(events)} events on the schedule")
    print(f"  {len(done)} completed | {len(live)} in progress | {len(upcoming)} upcoming | {len(canceled)} canceled")

    # only completed events have a real winner (scheduled ones show the defending champion)
    wins = {}
    for e in done:
        name = (e.get("winnerAthlete") or {}).get("name")
        if name:
            wins[name] = wins.get(name, 0) + 1
    print(f"  {len(wins)} different winners in {sum(wins.values())} individual events")
    multi = sorted(((n, c) for n, c in wins.items() if c > 1), key=lambda kv: (-kv[1], kv[0]))
    print("Multiple winners: " + ", ".join(f"{n} {c}" for n, c in multi))

    print("\nLatest completed events")
    for e in done[-3:][::-1]:
        w = e.get("winnerAthlete") or {}
        print(f"  {e['date']:<14}{e['name']:<52}{w.get('name', '-')} ({e.get('score', '')})")
    return done[-1]


def leaderboard(event, top=10):
    data = call("/leaderboard", eventId=event_id(event))["events"][0]
    comp = data["competitions"][0]
    players = sorted(comp["competitors"], key=lambda c: c["sortOrder"])
    made_cut = [p for p in players if p["status"]["type"]["name"] != "STATUS_CUT"]
    course = data["courses"][0]
    print(f"\n{data['name']} - {course['name']}, par {course['shotsToPar']}, purse {data['displayPurse']}")
    print(f"Winner: {data['winner']['displayName']} | {len(players)} players, {len(made_cut)} made the cut")
    print(f"{'Pos':<5}{'Player':<22}{'To par':<8}{'Rounds':<14}{'Money':>10}")
    for p in players[:top]:
        rounds = "-".join(str(int(l["value"])) for l in p["linescores"] if not l.get("isPlayoff") and l.get("value"))
        print(f"{p['status']['position']['displayName']:<5}{p['athlete']['displayName']:<22}"
              f"{p['score']['displayValue']:<8}{rounds:<14}{'$' + format(p['earnings'], ','):>10}")


if __name__ == "__main__":
    latest = season_recap(sys.argv[1] if sys.argv[1:] else "2026")
    leaderboard(latest)
