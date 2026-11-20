"""Minute-by-minute timeline of a finished match: goals, cards and substitutions (Soccer Live Info API).

Usage:
    export RAPIDAPI_KEY=your_key
    python soccer_match_timeline.py aVUGdLT3lNb2iCEqFHhBv
"""
import os
import sys
import time

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


def minute(e):
    p = e.get("period")
    return f"{p['minute']}+{p['extra']}'" if p and p.get("extra") else (f"{p['minute']}'" if p else "-")


def timeline(match_id):
    data = call(f"/matches/{match_id}/events")
    # The API lists events newest first, so reverse them.
    for e in reversed(data["events"]):
        t = e["type"]
        if t == "GOAL":
            line = f"GOAL {e['side']} {e['scorer']['name']} ({e['score']['teamA']}-{e['score']['teamB']})"
            if e.get("assist"):
                line += f", assist {e['assist']['name']}"
        elif t == "SUBSTITUTION":
            line = f"SUB  {e['side']} {e['in']['name']} on, {e['out']['name']} off"
        elif t.startswith("CARD"):
            line = f"{t.replace('_', ' ')} {e['side']} {e['player']['name']}"
        else:
            line = t.replace("PERIOD_", "").replace("_", " ").title()
        print(f"{minute(e):>6}  {line}")
    return data


if __name__ == "__main__":
    timeline(sys.argv[1])
