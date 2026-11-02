"""Stock performance snapshot. Uses the Investing.com Ultimate API on RapidAPI."""
import os, sys, time
import requests

HOST = "investing-com-ultimate-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def stock(symbol):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/v2/stocks", headers=HEADERS,
                         params={"symbol": symbol}, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(symbols):
    print("SYMBOL".ljust(8) + "PRICE".rjust(9) + "1D".rjust(8) + "1M".rjust(8) +
          "YTD".rjust(8) + "1Y".rjust(8) + "  FROM 52W HIGH")
    for symbol in symbols:
        d = stock(symbol)
        p, perf, rng = d["price"], d["performance"], d["range_52_weeks"]
        off_high = (p["last"] / rng["high"] - 1) * 100
        print(symbol.upper().ljust(8) + f"{p['last']:9.2f}" + f"{perf['1d']:+7.1f}%" +
              f"{perf['1m']:+7.1f}%" + f"{perf['ytd']:+7.1f}%" + f"{perf['1y']:+7.1f}%" +
              f"  {off_high:+.1f}%  {d['name']}")


if __name__ == "__main__":
    main(sys.argv[1:] or ["AAPL", "MSFT", "NVDA"])
