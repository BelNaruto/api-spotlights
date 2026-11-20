"""Audit the UFC rankings returned by the MMA API on RapidAPI.

GET /rankings-ufc returns a list of `rankings`. Each item has a division `name` and 15 `ranks`.
The script prints the top 2 of every numbered list and compares it with the repeated lists
that have no rank numbers.

Usage:
    export RAPIDAPI_KEY=your_key
    python mma_ufc_rankings_audit.py
"""
import os
import time

import requests

HOST = "mma-api1.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            return r.json()
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def split(rankings):
    """Numbered lists (rank filled in) and unnumbered lists (rank empty)."""
    numbered = [d for d in rankings if d["ranks"] and d["ranks"][0]["rank"]]
    plain = [d for d in rankings if d["ranks"] and not d["ranks"][0]["rank"]]
    return numbered, plain


def report(data):
    numbered, plain = split(data["rankings"])
    print(f"{len(data['rankings'])} lists: {len(numbered)} numbered, {len(plain)} without rank numbers\n")
    print("Numbered lists (top 2)")
    for d in numbered:
        print(f"  {d['name'][:32]:<33}1. {d['ranks'][0]['name']:<22}2. {d['ranks'][1]['name']}")
    print("\nUnnumbered list leader vs numbered #1 (same division name)")
    first = {}
    for d in numbered:
        first.setdefault(d["name"], d["ranks"][0]["name"])
    for d in plain:
        lead, num = d["ranks"][0]["name"], first.get(d["name"])
        flag = "same" if lead == num else f"differs (numbered #1: {num})"
        print(f"  {d['name'][:22]:<23}{lead:<22}{flag}")


if __name__ == "__main__":
    report(call("/rankings-ufc"))
