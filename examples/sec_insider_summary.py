"""90-day insider buy/sell summary for a list of tickers (SEC Filings API on RapidAPI).

Uses GET /v1/insiders/{ticker}/summary?days=90, which adds up the Form 4 filings of the last 90 days.

Usage:
    export RAPIDAPI_KEY=your_key
    python sec_insider_summary.py AAPL
    python sec_insider_summary.py AAPL MSFT NVDA
"""
import os
import sys
import time

import requests

HOST = "sec-filings-api2.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if body.get("error"):
                raise RuntimeError(body.get("message"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def verdict(d):
    if d["sharesSold"] == 0 and d["sharesBought"] == 0:
        return "no open-market activity"
    if d["netShares"] < 0:
        return "net selling"
    return "net buying"


def report(rows):
    print(f"{'ticker':<7}{'insiders':>9}{'filings':>8}{'bought':>10}{'sold':>10}{'net':>10}{'est. USD sold':>16}  verdict")
    for ticker, d in rows:
        print(f"{ticker:<7}{d['distinctInsidersReporting']:>9}{d['filingsAnalyzed']:>8}"
              f"{d['sharesBought']:>10,}{d['sharesSold']:>10,}{d['netShares']:>10,}"
              f"{d['estimatedUsdSold']:>16,.0f}  {verdict(d)}")


if __name__ == "__main__":
    tickers = [t.upper() for t in sys.argv[1:]] or ["AAPL"]
    rows = [(t, call(f"/v1/insiders/{t}/summary", days=90)) for t in tickers]
    report(rows)
    for t, d in rows:
        if d["sharesSold"]:
            print(f"\n{t}: insiders bought {d['sharesBought'] / d['sharesSold']:.2f} shares for every share sold "
                  f"(API buySellRatio {d['buySellRatio']}), estimated USD bought: {d['estimatedUsdBought']:,.0f}")
