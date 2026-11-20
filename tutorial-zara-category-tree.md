---
title: Map Zara's full category tree with Python
image: /assets/zara-category-tree-og.jpg
description: A Python script that downloads Zara's category tree and counts sections, categories, leaves and depth, using the Zara Data API on RapidAPI.
---

# Map Zara's full category tree with Python

One call returns Zara's whole navigation tree. The script walks it and reports how big each section is, which is handy for planning a catalogue crawl. It uses the [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /categories` with `language` (for example `en_US`). The tree is in `data.categories`. Each node has `id`, `key`, `name`, `sectionName`, `subcategories` and an `seo.keyword`. Full script: [`examples/zara_category_tree.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/zara_category_tree.py).

```python
cats = call("/categories", language="en_US")["categories"]
for c in cats:
    print(c["name"], len(c["subcategories"]))
```

```bash
python zara_category_tree.py
```

## Real output (20 Nov 2026)

**8 sections, 2,835 categories, 2,356 leaf categories, 6 levels deep.**

| Section | Categories | Top-level children |
|---------|-----------|--------------------|
| KIDS | 1,207 | 26 |
| MAN | 496 | 18 |
| ZARA HOME | 424 | 108 |
| MASSIMO DUTTI | 317 | 6 |
| WOMAN | 288 | 18 |
| BEAUTY | 68 | 10 |
| ZARA SRPLS | 24 | 4 |
| REFORM | 11 | 3 |

2,707 of the nodes carry an `seo.keyword`, which you can use as a URL-friendly slug.

## Ideas

- Pick the `WOMAN` sub-tree and crawl each leaf with `/search`.
- Diff the tree weekly to spot new collections.
