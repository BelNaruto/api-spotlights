"""Audit Fashion Nova's collections: biggest, empty and duplicated ones (Fashion Nova API).

Usage:
    export RAPIDAPI_KEY=your_key
    python fashionnova_collections_audit.py
"""
import os
import time
from collections import defaultdict

import requests

HOST = "fashion-nova-api.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}


def call(path, **params):
    for attempt in range(3):
        r = requests.get(f"https://{HOST}{path}", headers=HEADERS, params=params, timeout=60)
        if r.ok:
            body = r.json()
            if not body.get("success"):
                raise RuntimeError(body.get("error"))
            return body["data"]
        time.sleep(2 * (attempt + 1))
    r.raise_for_status()


def audit():
    collections = call("/collections", page=1, perPage=100)["collections"]
    filled = [c for c in collections if c["products_count"] > 0]
    print(f"{len(collections)} collections on page 1: {len(filled)} with products, {len(collections) - len(filled)} empty\n")
    print(f"{'Collection':<34}{'Handle':<22}{'Products':>9}")
    for c in sorted(filled, key=lambda c: -c["products_count"])[:8]:
        print(f"{c['title'][:33]:<34}{c['handle'][:21]:<22}{c['products_count']:>9,}")
    by_title = defaultdict(list)
    for c in filled:
        by_title[c["title"]].append(c["handle"])
    for title, handles in by_title.items():
        if len(handles) > 1:
            print(f"\nDuplicate title '{title}': {', '.join(handles)}")
    newest = max(collections, key=lambda c: c["updated_at"])
    print(f"\nMost recently updated: {newest['title']} ({newest['updated_at']})")
    return collections


if __name__ == "__main__":
    audit()
