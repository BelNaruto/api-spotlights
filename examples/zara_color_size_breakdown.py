import os
import sys
import time

import requests

HOST = "zara-data-api.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}
LETTER_SIZES = ("xs", "s", "m", "l", "xl", "xxl")


def filters(query, section="WOMAN"):
    for attempt in range(3):
        r = requests.get(
            f"https://{HOST}/search/filters",
            headers=HEADERS,
            params={"query": query, "section": section, "language": "en_US"},
            timeout=60,
        )
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return {f["type"]: f for f in r.json()["data"]["filters"]}


def bars(values, title):
    total = sum(v["count"] for v in values)
    print(f"\n{title} ({total} items)")
    for v in sorted(values, key=lambda v: v["count"], reverse=True):
        share = 100 * v["count"] / total
        print(f"  {v['title'].ljust(10)} {str(v['count']).rjust(4)}  {round(share / 2) * '#'} {share:.0f}%")


def main(query):
    found = filters(query)
    price = found["price"]
    # price filter values are in cents and the response has no currency
    print(f"'{query}' price range: {price['minValue'] / 100:.2f} to {price['maxValue'] / 100:.2f}")
    bars(found["color"]["values"], "Colours")
    sizes = [v for v in found["size"]["values"] if v["id"] in LETTER_SIZES]
    bars(sizes, "Letter sizes")


if __name__ == "__main__":
    main((sys.argv[1:] + ["jeans"])[0])
