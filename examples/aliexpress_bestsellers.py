"""Rank AliExpress search results by units sold. Uses the AliExpress Data API on RapidAPI."""
import os, sys, time
import requests

HOST = "aliexpress-data.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def search(query, page=1):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/search/products", headers=HEADERS, timeout=60,
                         params={"query": query, "country": "us", "currency": "USD", "page": page})
        if r.ok:
            return r.json()["data"]["items"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def units_sold(text):
    """Turn '184 sold' or '1K+ sold' into a number."""
    word = (text or "").split(" ")[0].replace("+", "").replace(",", "")
    if not word:
        return 0
    if word.endswith("K"):
        return int(float(word[:-1]) * 1000)
    return int(float(word)) if word.replace(".", "").isdigit() else 0


def main(query, pages=2, top=10):
    items = []
    for page in range(1, pages + 1):
        items += search(query, page)
    items.sort(key=lambda i: units_sold(i["trade"].get("tradeDesc")), reverse=True)
    for item in items[:top]:
        sold = units_sold(item["trade"].get("tradeDesc"))
        stars = (item.get("evaluation") or {}).get("starRating") or "-"
        print(f"{sold:6d} sold  {stars} stars  {item['title']['displayTitle'][:50]}")
        print("        " + item["url"])


if __name__ == "__main__":
    main((sys.argv[1:] + ["phone case"])[0])
