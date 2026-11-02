import os
import sys
import time

import requests

HOST = "investing-com-ultimate-api.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}


def dividends(symbol, country="US"):
    # country is required: the same ticker can exist in several countries
    for attempt in range(3):
        r = requests.get(
            f"https://{HOST}/v2/stocks/dividends",
            headers=HEADERS,
            params={"symbol": symbol, "country": country},
            timeout=60,
        )
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()


def main(symbol, country="US"):
    body = dividends(symbol, country)
    data, meta = body["data"], body["meta"]
    summary, history = data["summary"], data["history"]
    print(f"{meta['instrument']['name']} ({symbol.upper()}, {country.upper()}) in {meta['currency']}")
    print(f"Annualized payout {summary['annualized_payout']}  yield {summary['dividend_yield']:.2f}%  5y growth {summary['five_year_growth']:.1f}%")
    print("\nEX-DATE      PAID         AMOUNT")
    for item in history[:6]:
        print(f"{item['ex_date']}   {item['payment_date']}   {item['amount']:.2f}  {item['frequency']}")
    if history[4:]:
        newest, year_ago = history[0]["amount"], history[4]["amount"]
        print(f"\nLatest payment vs a year earlier: {100 * (newest / year_ago - 1):+.1f}%")


if __name__ == "__main__":
    args = sys.argv[1:] + ["AAPL", "US"]
    main(args[0], args[1])
