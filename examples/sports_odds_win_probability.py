"""Turn NFL moneylines and Super Bowl futures into win probabilities (Sports Odds API).

Moneylines include the bookmaker's margin, so the two raw probabilities add up to more than 100%.
The script shows the margin and the fair (margin-free) win chance, at the open and at the close.

Usage:
    export RAPIDAPI_KEY=your_key
    python sports_odds_win_probability.py
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


def implied(american):
    """American odds (as a string like '-600' or '+440') to a raw probability."""
    n = float(american)
    return 100 / (n + 100) if n > 0 else -n / (-n + 100)


def fair_home(home_odds, away_odds):
    h, a = implied(home_odds), implied(away_odds)
    return h / (h + a), h + a - 1


def games(week):
    rows = []
    for event in week["events"]:
        comp = event["competitions"][0]
        odds = (comp.get("odds") or [None])[0]
        if not odds:
            continue
        home = next(c for c in comp["competitors"] if c["homeAway"] == "home")["team"]["abbreviation"]
        away = next(c for c in comp["competitors"] if c["homeAway"] == "away")["team"]["abbreviation"]
        ml = odds["moneyline"]
        p_open, m_open = fair_home(ml["home"]["open"]["odds"], ml["away"]["open"]["odds"])
        p_close, m_close = fair_home(ml["home"]["close"]["odds"], ml["away"]["close"]["odds"])
        rows.append({"game": f"{away} @ {home}", "home": home, "away": away, "p_open": p_open, "p_close": p_close,
                     "margin": m_close})
    return rows


def report(data):
    week = data["lines"][0]
    rows = sorted(games(week), key=lambda r: -abs(r["p_close"] - r["p_open"]))
    print(f"{week['displayValue']}: fair home win chance, open vs close\n")
    print(f"{'Game':<10}{'Home open':>10}{'Home close':>11}{'Shift':>8}{'Margin':>8}")
    for r in rows:
        print(f"{r['game']:<10}{r['p_open']:>9.0%}{r['p_close']:>11.0%}{(r['p_close'] - r['p_open']) * 100:>+7.0f}pt{r['margin']:>8.1%}")
    avg_margin = sum(r["margin"] for r in rows) / len(rows)
    print(f"\nAverage bookmaker margin on the closing moneyline: {avg_margin:.1%}")

    future = data["futures"][0]
    books = future["future"]["books"]
    probs = [(b["team"]["displayName"], b["displayValue"], implied(b["displayValue"])) for b in books]
    print(f"\n{future['futureType']['displayValue']} futures ({len(books)} teams listed, "
          f"market active: {future['futureType']['active']})")
    for name, odds, p in probs:
        print(f"  {name:<24}{odds:>7}  {p:>6.1%}")
    print(f"Listed teams add up to {sum(p for _, _, p in probs):.0%} before the other {32 - len(books)} teams.")
    return rows, probs


if __name__ == "__main__":
    report(call("/nfl/odds"))
