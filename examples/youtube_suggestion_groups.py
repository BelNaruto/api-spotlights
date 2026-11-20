"""Group YouTube search suggestions by the next word (YouTube Data API on RapidAPI).

Uses GET /search/suggestion?query=... Type the start of a search and the API returns what people
search next. The script groups the suggestions by the word that follows your seed.

Usage:
    export RAPIDAPI_KEY=your_key
    python youtube_suggestion_groups.py "how to"
"""
import os
import sys
import time
from collections import defaultdict

import requests

HOST = "youtube-data19.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("message"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def group(seed, suggestions):
    groups = defaultdict(list)
    for s in suggestions:
        rest = s[len(seed):].split()
        groups[rest[0] if rest else "(seed only)"].append(" ".join(rest[1:]) or "-")
    return groups


def report(data):
    seed, sugg = data["query"], data["suggestions"]
    print(f"{len(sugg)} suggestions for '{seed}'\n")
    for word, rest in sorted(group(seed, sugg).items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print(f"{word:<10}{len(rest)}  {'; '.join(rest)}")
    print("\nLongest:", max(sugg, key=len))


if __name__ == "__main__":
    seed = " ".join(sys.argv[1:]) or "how to"
    report(call("/search/suggestion", query=seed))
