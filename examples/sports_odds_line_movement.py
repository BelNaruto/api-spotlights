"""Show how NFL betting lines moved from open to close (Sports Odds API).

Usage:
    export RAPIDAPI_KEY=your_key
    python sports_odds_line_movement.py
"""
import os
import time

import requests

HOST = "sports-odds-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("status") != "success":
                raise RuntimeError(body.get("error"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def num(text):
    """'-16.5' -> -16.5, 'o44.5' -> 44.5, '+210' -> 210."""
    return float(str(text).lstrip("ou"))


def moves(week):
    rows = []
    for event in week["events"]:
        comp = event["competitions"][0]
        odds = (comp.get("odds") or [None])[0]
        if not odds:
            continue
        home = next(c for c in comp["competitors"] if c["homeAway"] == "home")["team"]["abbreviation"]
        away = next(c for c in comp["competitors"] if c["homeAway"] == "away")["team"]["abbreviation"]
        sp, tot, ml = odds["pointSpread"]["home"], odds["total"]["over"], odds["moneyline"]["home"]
        s_open, s_close = num(sp["open"]["line"]), num(sp["close"]["line"])
        t_open, t_close = num(tot["open"]["line"]), num(tot["close"]["line"])
        rows.append({
            "game": f"{away} @ {home}", "day": comp["date"][5:10], "home": home, "away": away,
            "s_open": s_open, "s_close": s_close, "s_move": s_close - s_open,
            "t_open": t_open, "t_close": t_close, "t_move": t_close - t_open,
            "ml_open": num(ml["open"]["odds"]), "ml_close": num(ml["close"]["odds"]),
            "flip": (s_open < 0) != (s_close < 0) and s_open != 0 and s_close != 0,
        })
    return sorted(rows, key=lambda r: -abs(r["s_move"]))


def report(data):
    week = data["lines"][0]
    rows = moves(week)
    print(f"{week['displayValue']} ({len(rows)} games, odds from {data['provider']['displayName']})\n")
    print(f"{'Game':<10}{'Day':>6}  {'Home spread':>16}{'Move':>7}  {'Total':>13}{'Move':>7}  {'Home ML':>14}")
    for r in rows:
        print(f"{r['game']:<10}{r['day']:>6}  {r['s_open']:>+7g} -> {r['s_close']:>+6g}{r['s_move']:>+7g}  "
              f"{r['t_open']:>6g} -> {r['t_close']:>5g}{r['t_move']:>+7g}  {r['ml_open']:>+6g} -> {r['ml_close']:>+5g}")
    avg = sum(abs(r["s_move"]) for r in rows) / len(rows)
    flips = [r["game"] for r in rows if r["flip"]]
    print(f"\nAverage spread move: {avg:.1f} points. Favourite changed: {', '.join(flips) or 'none'}.")
    big_t = max(rows, key=lambda r: abs(r["t_move"]))
    print(f"Biggest total move: {big_t['game']} ({big_t['t_open']:g} -> {big_t['t_close']:g}).")
    return rows


if __name__ == "__main__":
    report(call("/nfl/odds"))
