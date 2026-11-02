"""Competitor Shopify store teardown. Uses the Shopify Stores Info API on RapidAPI."""
import os, sys, time
from collections import Counter
from statistics import median
import requests

HOST = "shopify-stores-info.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}


def get(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()


def teardown(domain, pages=2):
    info = get("/store/info", url=domain)
    products = []
    for page in range(1, pages + 1):
        data = get("/product/all", url=domain, page=page)
        products += data["products"]
        if not data["pagination"]["hasNextPage"]:
            break

    prices = [p["pricing"]["priceMin"] for p in products if p["pricing"]["priceMin"]]
    on_sale = [p for p in products if p["pricing"]["onSale"]]
    types = Counter(p["productType"] or "(none)" for p in products)

    print(f"{info['title']} ({domain})")
    print(f"  theme: {info['storeTheme']['name']}   currency: {info['storeCurrency']}")
    print(f"  catalogue: {info['availableProducts']} products, {info['publishedCollectionsCount']} collections")
    print(f"  ships to {len(info['shipstoCountries'])} countries")
    print(f"  sampled {len(products)} products: median price {median(prices):.2f}, "
          f"range {min(prices):.2f} to {max(prices):.2f}")
    print(f"  on sale: {len(on_sale)} of {len(products)} ({len(on_sale) / len(products):.0%})")
    print("  top types: " + ", ".join(f"{t} ({n})" for t, n in types.most_common(3)))


if __name__ == "__main__":
    for d in sys.argv[1:] or ["allbirds.com"]:
        teardown(d)
