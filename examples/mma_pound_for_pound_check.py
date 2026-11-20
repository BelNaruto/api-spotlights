"""Do the UFC pound-for-pound fighters also appear in a division ranking? (MMA API on RapidAPI)

GET /rankings-ufc returns the men's pound-for-pound list and one list per division. The script
looks up every pound-for-pound fighter in the division lists and prints the division and rank,
or "not in a division list".

Usage:
    export RAPIDAPI_KEY=your_key
    python mma_pound_for_pound_check.py
"""
import sys

from mma_ufc_rankings_audit import call, split

P4P = "Men's Pound-for-Pound Top Rank"
OTHER_P4P = "Women's Pound-for-Pound Top Rank"


def report(data):
    numbered, _ = split(data["rankings"])
    p4p = next(d for d in numbered if d["name"] == P4P)
    divisions = [d for d in numbered if d["name"] not in (P4P, OTHER_P4P)]
    where = {}
    for d in divisions:
        for r in d["ranks"]:
            where.setdefault(r["name"], (d["name"], r["rank"]))
    missing = 0
    print(f"{P4P}\n")
    for r in p4p["ranks"]:
        div = where.get(r["name"])
        if div is None:
            missing += 1
        text = f"{div[0]} #{div[1]}" if div else "not in a division list"
        print(f"  {r['rank']:>2}. {r['name']:<24}{text}")
    print(f"\n{missing} of {len(p4p['ranks'])} pound-for-pound fighters are not in any division list")


if __name__ == "__main__":
    report(call("/rankings-ufc"))
