"""Live stock watchlist in the terminal. Uses the Seeking Alpha API on RapidAPI."""
import os, re, sys, time
import requests

HOST = "seeking-alpha-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def find_id(ticker):
    """/search returns symbols with a numeric id (sa_id). Pick the exact ticker match."""
    symbols = call("/search", query=ticker, limit=10)["search_result"]["symbols"]
    for s in symbols:
        if s["name"].upper() == ticker.upper():
            return s["id"], re.sub(r"\x3c/?b\x3e", "", s["content"])  # strip highlight tags
    return None, None


def quote(sa_id):
    return call("/price", sa_id=sa_id)["real_time_quote"][0]


def main(tickers):
    rows = []
    for t in tickers:
        sa_id, name = find_id(t)
        if sa_id is None:
            print(f"{t}: not found")
            continue
        q = quote(sa_id)
        last, prev = q.get("last"), q.get("prev_close")
        change = (last - prev) / prev * 100 if last and prev else 0.0
        rows.append((change, t.upper(), name, last, q.get("volume"), q.get("info")))
    rows.sort(reverse=True)
    for change, t, name, last, volume, info in rows:
        print(t.ljust(7) + f"{last:10.2f}  {change:+6.2f}%  {name[:28].ljust(28)} ({info})")


if __name__ == "__main__":
    main(sys.argv[1:] or ["AAPL", "MSFT", "NVDA", "TSLA"])
