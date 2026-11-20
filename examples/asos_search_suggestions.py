"""Rank the ASOS search suggestions for a term by how many products they return (Asos API).

Usage:
    export RAPIDAPI_KEY=your_key
    python asos_search_suggestions.py jacket
"""
import os
import sys
import time

import requests

HOST = "asos-api6.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def suggestions(term):
    items = call("/product/search/autocomplete", query=term)["suggestions"]
    items.sort(key=lambda s: -s["numberOfResults"])
    total = sum(s["numberOfResults"] for s in items)
    print(f"{len(items)} suggestions for '{term}':\n")
    for s in items:
        bar = "#" * max(1, round(40 * s["numberOfResults"] / items[0]["numberOfResults"]))
        print(f"{s['searchTerm']:<46}{s['numberOfResults']:>6}  {bar}")
    print(f"\nSuggestions overlap, so their {total:,} results are not distinct products.")
    return items


if __name__ == "__main__":
    suggestions(sys.argv[1] if len(sys.argv) > 1 else "jacket")
