---
title: Rank ASOS search suggestions by demand with Python
image: /assets/asos-search-suggestions-og.jpg
description: A Python script that turns the ASOS autocomplete response into a ranked list of related searches with their result counts, using the Asos API on RapidAPI.
---

# Rank ASOS search suggestions with Python

Type a word and the autocomplete endpoint returns the related searches ASOS shows, each with how many products it matches. The script ranks them and draws a small bar chart. It uses the [Asos API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/asos-api6).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/search/autocomplete` with `query` (and an optional `limit`). The response has `data.suggestions`, each with a `searchTerm` and `numberOfResults`. Full script: [`examples/asos_search_suggestions.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/asos_search_suggestions.py).

```python
items = call("/product/search/autocomplete", query="jacket")["suggestions"]
for s in items:
    print(s["searchTerm"], s["numberOfResults"])
```

```bash
python asos_search_suggestions.py jacket
```

## Real output (20 Nov 2026)

Ten suggestions for `jacket`, in about 0.7 seconds:

| Suggestion | Results |
|------------|---------|
| jacket | 4,776 |
| women jacket | 3,409 |
| bomber jacket | 691 |
| funnel neck jacket | 632 |
| puffer jacket | 475 |
| leather jacket | 411 |
| puffer jacket women | 321 |
| faux fur jacket | 293 |
| adidas jacket | 71 |
| adidas originals x asos overhead track jacket | 2 |

## Things to know

- The suggestions overlap ("puffer jacket" and "puffer jacket women"), so adding the result counts does not give distinct products.
- The suggestion counts and the product search `itemCount` can differ: 4,776 against 6,227 for the same word.
- Very specific suggestions can return a handful of products (the Adidas track jacket returned 2), so filter by a minimum count before you use them as keywords.
- It is much faster than the product search, so call it first and search only for the suggestions you need.

## Ideas

- Feed the top suggestions into the search snapshot script.
- Run it for a list of garments and see which one has the most long-tail searches.
