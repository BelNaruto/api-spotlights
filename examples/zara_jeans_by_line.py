import os
import sys
import time

import requests

HOST = "zara-data-api.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}
LINES = ("TRF", "Z1975", "ZW")


def search(query, section="WOMAN"):
    # section defaults to HOME, so always send it for fashion searches
    for attempt in range(3):
        r = requests.get(
            f"https://{HOST}/search",
            headers=HEADERS,
            params={"query": query, "section": section, "perPage": 36, "language": "en_US"},
            timeout=60,
        )
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()["data"]


def main(query):
    data = search(query)
    prices = {}
    skipped = 0
    for product in data["products"]:
        content = product["content"]
        first = content["name"].split(" ")[0].upper()
        line = first if first in LINES else "OTHER"
        price = (content["colors"][0] if content["colors"] else {}).get("price")
        if price is None:
            skipped += 1
            continue
        prices.setdefault(line, []).append(float(price))
    print(f"{data['pagination']['totalResults']} results for '{query}', first {len(data['products'])} analysed")
    print("\nLINE".ljust(10) + "ITEMS".rjust(6) + "MIN".rjust(9) + "AVG".rjust(9) + "MAX".rjust(9))
    for line, values in sorted(prices.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
        print(line.ljust(9) + str(len(values)).rjust(6) + f"{min(values):9.2f}" + f"{sum(values) / len(values):9.2f}" + f"{max(values):9.2f}")
    if skipped:
        print(f"\n{skipped} product(s) skipped because the API returned no price")


if __name__ == "__main__":
    main((sys.argv[1:] + ["jeans"])[0])
