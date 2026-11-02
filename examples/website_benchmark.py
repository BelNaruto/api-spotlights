"""Benchmark websites by traffic and rank. Uses the Similar Web API on RapidAPI."""
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
