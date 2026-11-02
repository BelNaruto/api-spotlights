"""Which sizes are listed most for a Vinted search, and which get the most favourites. Uses the Vinted API on RapidAPI."""
import os, sys, time
from collections import defaultdict
import requests

HOST = "vinted-api3.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def search(query, country="us", per_page=40):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/search", headers=HEADERS, timeout=60,
                         params={"query": query, "country": country, "perPage": per_page})
        if r.ok:
            return r.json()["items"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def main(query):
    sizes = defaultdict(list)
    for item in search(query):
        size = (item.get("size_title") or "no size").split(" / ")[0]
        sizes[size].append(item["favourite_count"])
    print(f"{sum(len(v) for v in sizes.values())} listings for '{query}'\n")
    print("SIZE".ljust(10) + "LISTINGS".rjust(9) + "AVG FAVS".rjust(10))
    for size, favs in sorted(sizes.items(), key=lambda kv: len(kv[1]), reverse=True)[:8]:
        print(size.ljust(10) + str(len(favs)).rjust(9) + f"{sum(favs) / len(favs):10.1f}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["levi 501"])[0])
