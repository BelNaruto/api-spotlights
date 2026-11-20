"""Match preview for any two tennis players: head-to-head + model prediction.

Usage:
    export RAPIDAPI_KEY=your_key
    python tennis_match_preview.py 3623 3782 hard
    (player ids come from /rankings or /players/search)
"""
import os
import sys
import time

import requests

HOST = "tennis-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    """GET an endpoint and return the `data` part of the envelope (retries 5xx)."""
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def preview(p1, p2, surface="hard"):
    h2h = call("/h2h", player1=p1, player2=p2, limit=5)
    pred = call("/predictions/match", player1=p1, player2=p2, surface=surface, bestOf=3)

    a, b = h2h["player1"], h2h["player2"]
    rank = pred["components"]["ranking"]
    print(f"{a['name']} ({a['countryCode']}, #{rank['player1']['rank']}) vs "
          f"{b['name']} ({b['countryCode']}, #{rank['player2']['rank']})")

    s = h2h["summary"]
    print(f"Head-to-head: {s['player1']}-{s['player2']} in {s['matches']} meetings")
    print("  " + " | ".join(f"{name} {v['player1']}-{v['player2']}" for name, v in s["bySurface"].items()))

    last = h2h["lastMeeting"]
    winner = a["name"] if last["winnerId"] == a["id"] else b["name"]
    print(f"Last meeting: {last['tournament']} {last['year']} {last['round']} - {winner} won {last['score']}")

    p = pred["prediction"]
    pr = p["probabilities"]
    print(f"Prediction on {pred['surface']} (best of {pred['bestOf']}): "
          f"{a['name']} {pr['player1'] * 100:.1f}% - {b['name']} {pr['player2'] * 100:.1f}% "
          f"(confidence: {p['confidence']})")
    print(f"Most likely score: {p['predictedScore']} | chance of a deciding set: {p['goesTheDistance'] * 100:.1f}%")

    elo = pred["components"]["elo"]
    print(f"Elo ({pred['surface'].lower()}): {elo['player1']['used']} vs {elo['player2']['used']}")
    form = pred["components"]["form"]
    print(f"Form, last {form['player1']['last']}: {form['player1']['form']} vs {form['player2']['form']}")


if __name__ == "__main__":
    args = sys.argv[1:]
    preview(args[0] if len(args) > 0 else "3623",
            args[1] if len(args) > 1 else "3782",
            args[2] if len(args) > 2 else "hard")
