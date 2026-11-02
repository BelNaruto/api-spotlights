"""Find the cheapest Vinted listings for a search. Uses the Vinted API on RapidAPI."""
import os, sys, time
import requests

HOST = "vinted-api3.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def search(query, country="us", order="price_low_to_high", per_page=96):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/search", headers=HEADERS, timeout=60,
                         params={"query": query, "country": country,
                                 "orderBy": order, "perPage": per_page})
        if r.ok:
            return r.json()["items"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(query, max_price, country, top=10):
    shown = 0
    for item in search(query, country):
        total = float(item["total_item_price"]["amount"])
        if min(total, max_price) != total:
            break  # sorted by price, so everything after this is too expensive
        cur = item["total_item_price"]["currency_code"]
        print(f"{total:7.2f} {cur}  {item['favourite_count']:3d} favs  "
              f"{(item.get('brand_title') or '-')[:14].ljust(14)} {(item.get('size_title') or '-')[:6].ljust(6)} "
              f"{item['title'][:40]}")
        print("        " + item["url"])
        shown += 1
        if shown == top:
            break
    if shown == 0:
        print("No listings under that price.")


if __name__ == "__main__":
    a = sys.argv[1:] + ["hoodie", "20", "us"][len(sys.argv) - 1:]
    main(a[0], float(a[1]), a[2])
