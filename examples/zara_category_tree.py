"""Map Zara's whole category tree: sections, depth and leaf categories (Zara Data API).

Usage:
    export RAPIDAPI_KEY=your_key
    python zara_category_tree.py
"""
import os
import time

import requests

HOST = "zara-data-api.p.rapidapi.com"
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


def walk(node, depth=1):
    """Return (nodes, deepest level, leaves) for a category and everything under it."""
    subs = node.get("subcategories") or []
    if not subs:
        return 1, depth, 1
    nodes, deepest, leaves = 1, depth, 0
    for s in subs:
        n, d, l = walk(s, depth + 1)
        nodes += n
        deepest = max(deepest, d)
        leaves += l
    return nodes, deepest, leaves


def category_tree():
    cats = call("/categories", language="en_US")["categories"]
    total = deepest = leaves = 0
    print(f"{'Section':<16}{'Categories':>11}{'Leaves':>8}{'Top-level children':>20}")
    for c in cats:
        n, d, l = walk(c)
        total += n
        deepest = max(deepest, d)
        leaves += l
        print(f"{c['name']:<16}{n:>11}{l:>8}{len(c.get('subcategories') or []):>20}")
    print(f"\n{len(cats)} sections, {total} categories, {leaves} leaves, {deepest} levels deep")
    return cats


if __name__ == "__main__":
    category_tree()
