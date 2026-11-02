import os
import sys
import time

import requests

HOST = "aliexpress-data.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
    "X-RapidAPI-Host": HOST,
}


def search(query, country="us", currency="USD"):
    for attempt in range(3):
        r = requests.get(
            f"https://{HOST}/search/products",
            headers=HEADERS,
            params={"query": query, "country": country, "currency": currency, "page": 1},
            timeout=60,
        )
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(2)
            continue
        r.raise_for_status()
        return r.json()["data"]["items"]


def sold(item):
    # tradeDesc looks like "184 sold" or "10,000+ sold"; some items have none
    text = (item.get("trade") or {}).get("tradeDesc") or ""
    digits = "".join(ch for ch in text.split(" ")[0] if ch.isdigit())
    return int(digits) if digits else 0


def main(query, min_sold=500, top=8):
    items = search(query)
    rated = []
    for item in items:
        stars = (item.get("evaluation") or {}).get("starRating")
        if stars is not None and sold(item) >= min_sold:
            rated.append((stars, sold(item), item["title"]["displayTitle"]))
    rated.sort(reverse=True)
    print(f"{len(items)} results for '{query}', {len(rated)} with {min_sold}+ sold and a rating")
    for stars, units, title in rated[:top]:
        print(f"{stars}  {str(units).rjust(6)}+  {title[:24]}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["led strip lights"])[0])
