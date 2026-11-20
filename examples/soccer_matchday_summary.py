"""Match day summary: results, goals and biggest wins across every competition (Soccer Live Info API).

Usage:
    export RAPIDAPI_KEY=your_key
    python soccer_matchday_summary.py 2026-11-14
"""
import os
import sys
import time
from collections import Counter

import requests

HOST = "soccer-football-live-info.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=90)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body)
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def summary(date):
    comps = call("/matches", date=date)
    matches = [dict(m, comp=c["competition"]["name"]) for c in comps for m in c["matches"]]
    status = Counter(m["status"] for m in matches)
    done = [m for m in matches if m["status"] == "RESULT"]
    goals = sum(m["score"]["teamA"] + m["score"]["teamB"] for m in done)
    print(f"{date}: {len(matches)} matches in {len(comps)} competitions  {dict(status)}")
    print(f"{goals} goals in {len(done)} finished matches ({goals / len(done):.2f} per match)")
    print(f"home wins {sum(m['score']['teamA'] > m['score']['teamB'] for m in done)}, "
          f"draws {sum(m['score']['teamA'] == m['score']['teamB'] for m in done)}, "
          f"away wins {sum(m['score']['teamA'] < m['score']['teamB'] for m in done)}\n")
    print("Biggest margins:")
    for m in sorted(done, key=lambda m: -abs(m["score"]["teamA"] - m["score"]["teamB"]))[:5]:
        print(f"  {m['teamA']['short']} {m['score']['teamA']}-{m['score']['teamB']} {m['teamB']['short']}  ({m['comp']})")
    return matches


if __name__ == "__main__":
    summary(sys.argv[1])
