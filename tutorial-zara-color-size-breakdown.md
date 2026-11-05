---
image: /assets/vinted-deal-finder-og.jpg
title: Chart the colours and sizes of any Zara search in Python
description: A short Python script that uses the Zara filters endpoint to print the price range and a colour and size breakdown for any search, using the Zara Data API on RapidAPI.
---

# Chart the colours and sizes of any Zara search in Python

In this tutorial you will build a script that shows how a Zara search is made up: the price range, how many items come in each colour and how many in each letter size, drawn as a text bar chart. It uses the [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The filters endpoint (`/search/filters`) takes `query`, `section` and `language`. It returns `data.filters`, a list with three entries: `price` (with `minValue` and `maxValue` in cents, no currency in the response), `color` and `size`, each with `values` that have an `id`, a `title` and a `count`. The size list mixes several systems (letters, numbers and US sizes), so the script keeps only the letter sizes.

## 3. The script

Save this as `zara_color_size_breakdown.py`. It retries temporary server errors.

```python
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
```

## 4. Run it

```bash
python zara_color_size_breakdown.py jeans
```

Real output for a live jeans search in the WOMAN section:

```
'jeans' price range: 25.90 to 349.00

Colours (571 items)
  Blue        368  ################################ 64%
  Black        52  ##### 9%
  White        41  #### 7%
  Printed      29  ### 5%
  Green        18  ## 3%
  Gray         17  # 3%
  Brown        13  # 2%
  Beige        12  # 2%
  Red           8  # 1%
  Pink          7  # 1%
  Magenta       2   0%
  Orange        2   0%
  Khaki         1   0%
  Yellow        1   0%

Letter sizes (582 items)
  S           119  ########## 20%
  M           115  ########## 20%
  L           114  ########## 20%
  XS          104  ######### 18%
  XL           94  ######## 16%
  XXL          36  ### 6%
```

The complete script is in [examples/zara_color_size_breakdown.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/zara_color_size_breakdown.py).

## Tips

- Pass the `id` of a colour as `filters[color]` to the search endpoint to list only those items.
- Change `section` to `MAN` to compare with the men's range.
- Use the price range to build a price slider.

## Next steps

- [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
