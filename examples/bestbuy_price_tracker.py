"""Track Best Buy prices and print every drop. Uses the BestBuy USA API on RapidAPI."""
import json, os, sys, time
import requests

HOST = "bestbuy-usa.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}
STATE = "bestbuy_prices.json"


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            return body.get("data", body)
        if r.status_code in (502, 503, 504) and attempt != 2:
            time.sleep(int(r.headers.get("Retry-After", 5)))
            continue
        r.raise_for_status()


def search(query, limit=5):
    data = call("/search", query=query)
    products = {}
    for p in data["products"]:
        products.setdefault(p["skuId"], p)  # search can return the same sku twice
    return list(products.values())[:limit]


def current_price(sku):
    return call("/product/price", sku=sku)["customerPrice"]


def main(query):
    try:
        before = json.load(open(STATE))
    except FileNotFoundError:
        before = {}
    now = {}
    for p in search(query):
        sku = p["skuId"]
        price = current_price(sku)
        now[sku] = price
        score = (p.get("ratings") or {}).get("score")
        old = before.get(sku)
        if old is not None and price != old and price == min(price, old):
            print(f"DROP  ${old:.2f} to ${price:.2f}  {p['title']}  (rating {score})")
        else:
            print(f"      ${price:.2f}  {p['title']}  (rating {score})")
    json.dump({**before, **now}, open(STATE, "w"))


if __name__ == "__main__":
    main(sys.argv[1] if sys.argv[1:] else "sony headphones")
