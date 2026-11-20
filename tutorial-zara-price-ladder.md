---
title: Build a Zara price ladder by product family with Python
image: /assets/zara-price-ladder-og.jpg
description: A Python script that searches Zara by keyword and section and prints the price range and median per product family, using the Zara Data API on RapidAPI.
---

# Build a Zara price ladder with Python

Search Zara for any keyword and see how the prices spread across product families, such as jackets, coats and anoraks. The script also removes the duplicates the API can return. It uses the [Zara Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/zara-data-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /search` with `query`, `section` (`HOME`, `WOMAN`, `MAN` or `KID`), `page`, `perPage`, `language`, `sortBy` and filters. Results are in `data.products`; each has `content` with `name`, `reference`, `familyName`, `sectionName`, `pricing.value` and `colors`, plus a product `url`. `data.pagination` has `totalResults`. Full script: [`examples/zara_price_ladder.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/zara_price_ladder.py).

```python
data = call("/search", query="jacket", section="WOMAN", perPage=36, language="en_US")
for p in data["products"]:
    c = p["content"]
    print(c["familyName"], c["pricing"]["value"], c["name"])
```

```bash
python zara_price_ladder.py jacket WOMAN
```

## Real output (20 Nov 2026)

`jacket` in `WOMAN` matched **745 products**. The first page returned 36 items, of which **32 were unique** by `reference`.

| Family | Items | Min | Median | Max |
|--------|-------|-----|--------|-----|
| WIND-JACKET | 21 | 59.9 | 119.0 | 759.0 |
| COAT | 4 | 99.9 | 119.0 | 129.0 |
| ANORAK | 4 | 299.0 | 299.0 | 299.0 |
| TRENCH RAINCOAT | 1 | 99.9 | 99.9 | 99.9 |
| BLAZER | 1 | 229.0 | 229.0 | 229.0 |
| CARDIGAN | 1 | 69.9 | 69.9 | 69.9 |

The cheapest item was a stand-up collar bomber jacket at 59.9 and the most expensive were two limited-edition leather jackets at 759, both listed under `MAN` even though the search was in `WOMAN`.

## Things to know

- `section` defaults to `HOME`, so the documented example query `shoes` returned only Zara Home items (all 36 had brand group `zarahome`, such as slippers, home sandals and travel organizers). Always pass `section`.
- The same product can appear twice on one page (the same `reference`), so deduplicate before counting.
- `pricing.currency` comes back `null`, so the currency is implied by the store you query.
- A `WOMAN` search can include `MAN` items. Filter on `sectionName` if you need a strict split.

## Ideas

- Run it every week for `coat` and chart the median.
- Use `sortBy=price_asc` to find the cheapest piece in each family.
