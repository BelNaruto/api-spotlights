---
image: /assets/aliexpress-bestsellers-og.jpg
title: Find top-rated AliExpress products with real sales in Python
description: A short Python script that searches AliExpress and ranks products by star rating among those with real sales, using the AliExpress Data API on RapidAPI.
---

# Find top-rated AliExpress products with real sales in Python

In this tutorial you will build a script that searches AliExpress and ranks the results by star rating, keeping only products with a minimum number of units sold so tiny listings do not win. It uses the [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The search endpoint (`/search/products`) takes `query`, `country`, `currency` and `page`. It returns `data.items`; each item has `title.displayTitle`, `trade.tradeDesc` such as `184 sold` or `10,000+ sold`, and `evaluation.starRating`. Some items have no `evaluation` or `trade` key, so the script handles that.

## 3. The script

Save this as `aliexpress_top_rated.py`. It retries temporary server errors.

```python
import os
import sys
import time
from operator import ge

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
        if stars is not None and ge(sold(item), min_sold):
            rated.append((stars, sold(item), item["title"]["displayTitle"]))
    rated.sort(reverse=True)
    print(f"{len(items)} results for '{query}', {len(rated)} with {min_sold}+ sold and a rating")
    for stars, units, title in rated[:top]:
        print(f"{stars}  {str(units).rjust(6)}+  {title[:24]}")


if __name__ == "__main__":
    main((sys.argv[1:] + ["led strip lights"])[0])
```

## 4. Run it

```bash
python aliexpress_top_rated.py "led strip lights"
```

Real output for a live search (titles are cut to 24 characters):

```
60 results for 'led strip lights', 27 with 500+ sold and a rating
4.9   10000+  Dimmable 5V USB COB Led 
4.9   10000+  DC 5V USB LED Strips 283
4.9    5000+  Led Strip Light RGBW Add
4.9    3000+  Flexible and Even Cob Le
4.9    3000+  5V USB LED Strip Light F
4.9    3000+  5M 10M Per Roll COB LED 
4.9    2000+  Car RGB Ambient LED Ligh
4.9     900+  8mm PCB COB LED Strip DC
```

The complete script is in [examples/aliexpress_top_rated.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/aliexpress_top_rated.py).

## Tips

- Change `min_sold` to be stricter or looser.
- Run several keywords and compare the top products.
- Page through `page=2, 3` to widen the sample.

## Next steps

- [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
