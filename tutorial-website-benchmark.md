---
title: Benchmark any websites by traffic and rank in Python
description: A short Python script that compares websites by monthly visits, global rank and category rank, using the Similar Web API on RapidAPI.
image: /assets/similar-web-api-og.jpg
---

![Website benchmark](assets/similar-web-api.png)

# Benchmark any websites by traffic and rank in Python

In this tutorial you will build a script that takes a list of domains and prints a ranked comparison of their monthly visits, global rank and category rank. It is a quick way to size up competitors or prospects. It uses the [Similar Web API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/similar-web-api) and about 40 lines of Python.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key.

## 1. Get your API key

1. Open the [Similar Web API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/similar-web-api) and subscribe to the free **BASIC** plan.
2. Copy your `X-RapidAPI-Key` and export it:

```bash
export RAPIDAPI_KEY=your_key
```

## 2. Read a domain overview

`/domain/overview` takes a `url` and returns a `domain_overview` object with `monthlyVisits`, `rankings` (`globalRanking`, `categoryRanking`), `category`, `title` and more. The first call for a domain can take 10 to 15 seconds because fresh data is fetched, so we use a 60 second timeout and retry temporary server errors.

```python
import os, sys, time
import requests

HOST = "similar-web-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"], "X-RapidAPI-Host": HOST}

def overview(domain):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}/domain/overview", headers=HEADERS,
                         params={"url": f"https://{domain}"}, timeout=60)
        if r.ok:
            return r.json()["domain_overview"]
        if r.status_code in (500, 502, 503, 504) and attempt != 2:
            time.sleep(5)
            continue
        r.raise_for_status()
```

## 3. Build the comparison

Loop over the domains, skip any that fail, sort by traffic and print each one as a share of the leader.

```python
def main(domains):
    rows = []
    for d in domains:
        try:
            o = overview(d)
        except requests.RequestException as e:
            print(f"skip {d}: {e}")
            continue
        rows.append((o["monthlyVisits"], d, o["rankings"]["globalRanking"],
                     o["rankings"]["categoryRanking"], o["category"]))
    rows.sort(reverse=True)
    print("domain".ljust(20) + "visits/month".rjust(16) + "global rank".rjust(13) + "category rank".rjust(15) + "  category")
    top = rows[0][0] if rows else 1
    for visits, d, g, c, cat in rows:
        print(d.ljust(20) + f"{visits:,}".rjust(16) + str(g).rjust(13) + str(c).rjust(15)
              + f"  {cat}  ({visits / top:.0%} of leader)")

if __name__ == "__main__":
    main(sys.argv[1:] or ["amazon.com", "walmart.com", "ebay.com"])
```

## 4. Run it

```bash
python website_benchmark.py amazon.com walmart.com ebay.com
```

You get one line per site, sorted by traffic:

```
domain                  visits/month  global rank  category rank  category
amazon.com             2,555,045,157            9              1  E-commerce_And_Shopping/marketplace  (100% of leader)
```

The complete script is in [examples/website_benchmark.py](https://github.com/BelNaruto/api-spotlights/blob/main/examples/website_benchmark.py).

## Tips

- Pass the domain without a path. Results are cached, so repeat calls are faster.
- Save each run to a CSV to chart traffic over time.
- The API has more endpoints (top keywords, referrers, audience interest) that you can add as extra columns.

## Next steps

- [Similar Web API on RapidAPI](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/similar-web-api): all endpoints, plans and live playground.
- [API guide](similar-web-api): features and use cases.
- Questions? Message us on Telegram: [@pintoflow](https://t.me/pintoflow).
