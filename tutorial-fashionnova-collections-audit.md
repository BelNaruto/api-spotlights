---
title: Audit Fashion Nova's collections with Python
image: /assets/fashionnova-collections-audit-og.jpg
description: A Python script that lists Fashion Nova's collections with product counts, and flags empty and duplicated ones, using the Fashion Nova API on RapidAPI.
---

# Audit Fashion Nova's collections with Python

Fashion Nova organises its catalogue into hundreds of collections. This script fetches a page of them, shows the biggest and flags the empty and duplicated ones. It uses the [Fashion Nova API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/fashion-nova-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /collections` with `page` and `perPage` (up to 100). `data.collections` is a list; each has `id`, `title`, `handle`, `description`, `products_count`, `published_at` and `updated_at`. Use the `handle` with the collection-products endpoint to list what is inside. Full script: [`examples/fashionnova_collections_audit.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/fashionnova_collections_audit.py).

```python
collections = call("/collections", page=1, perPage=100)["collections"]
for c in sorted(collections, key=lambda c: -c["products_count"])[:5]:
    print(c["title"], c["handle"], c["products_count"])
```

```bash
python fashionnova_collections_audit.py
```

## Real output (20 Nov 2026)

Page 1 with `perPage=100` returned **100 collections: 51 with products and 49 empty**.

| Collection | Handle | Products |
|------------|--------|----------|
| All | all | 579,574 |
| All Women's Clothing | women | 36,229 |
| 75% Off Sale Blowout | summer-sale | 4,969 |
| 75% Off Sale Blowout | winter-blowout | 4,969 |
| 70% Off Sale | 70-off-sale | 2,790 |
| $10 Sale and Under | 10 | 2,352 |
| $5 & Under Sale for Women | 5-under | 2,072 |
| 420 Sale Collection | 420-collection | 1,135 |

The title "75% Off Sale Blowout" is used by two different handles (`summer-sale` and `winter-blowout`) with the same count. The most recently updated collections were `$12 Shoe Deals` and `$12 Nova Deals`, both updated on 20 Nov 2026.

## Things to know

- Almost half of the collections on this page are empty, so filter on `products_count` before building a menu.
- Collections overlap (`All` contains the others), so do not add the counts together.
- The response has no pagination block, so keep requesting pages until a page comes back short or empty.
- Only 2 of the 100 collections had an `image`.

## Ideas

- Track `products_count` for the sale collections to measure how fast the sale grows.
- Fetch the products of the biggest sale collection and compare it with the search results.
