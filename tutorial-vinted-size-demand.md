---
image: /assets/vinted-deal-finder-og.jpg
title: Find which sizes get the most interest on Vinted in Python
description: A short Python script that searches Vinted and shows how many listings and how many favourites each size gets, using the Vinted API on RapidAPI.
---

# Find which sizes get the most interest on Vinted in Python

In this tutorial you will build a script that searches Vinted for an item and groups the listings by size, showing how many listings and how many favourites on average each size has. It uses the [Vinted API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vinted-api3) and plain Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Vinted API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vinted-api3) on RapidAPI and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. The endpoint

The search endpoint (`/search`) takes `query`, `country` and `perPage`. It returns `items`; each item has `size_title`, `favourite_count`, `title` and more. This tutorial uses the first 40 listings of a search.

## 3. The script

Save this as `vinted_size_demand.py`. It retries temporary server errors.

```python
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
```

## 4. Run it

```bash
python vinted_size_demand.py "levi 501"
```

Real output from the first 40 live listings of a Levi 501 search:

```
40 listings for 'levi 501'

SIZE       LISTINGS  AVG FAVS
S                11       1.4
Other             8       0.5
XS                7       2.7
L                 3       0.7
M                 2       2.0
12                1       1.0
no size           1       0.0
W32               1       0.0
```

The complete script is in [examples/vinted_size_demand.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/vinted_size_demand.py).

## Tips

- Try other queries such as a sneaker model to compare size demand.
- Use favourites per listing as a quick demand signal when you decide what to buy and resell.
- Add more pages to the search for a larger sample.

## Next steps

- [Vinted API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/vinted-api3) on RapidAPI: all endpoints, plans and live playground.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
