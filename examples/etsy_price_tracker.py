"""Track Etsy listing prices and favorites. Uses the Etsy API on RapidAPI."""
import json, os, sys, time
import requests

HOST = "etsy-api2.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}
STATE = "etsy_prices.json"


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def search(query, limit=5):
    return call("/product/search", query=query)["results"][:limit]


def details(listing_id):
    return call("/product/description/v5", listingId=listing_id)


def main(query):
    try:
        before = json.load(open(STATE))
    except FileNotFoundError:
        before = {}
    now = {}
    for item in search(query):
        lid = str(item["listingId"])
        d = details(lid)
        price, favs = d["price"]["amount"], d["favorites"]
        if price is None:
            print(f"      no price yet  {item['title'][:60]}")
            continue
        now[lid] = {"price": price, "favorites": favs}
        old = before.get(lid)
        tag = "      "
        if old and price != old["price"] and price == min(price, old["price"]):
            tag = "DROP  "
        extra = f"  (+{favs - old['favorites']} favorites)" if old and favs != old["favorites"] else ""
        print(f"{tag}${price:.2f}  {favs} favorites  {item['title'][:50]}{extra}")
    json.dump({**before, **now}, open(STATE, "w"))


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "handmade candle")
