---
title: Are 3-star AliExpress reviews really complaints? A Python check
image: /assets/aliexpress-three-star-reviews-og.jpg
description: A Python script that reads the 3-star reviews of an AliExpress product with the AliExpress Data API on RapidAPI and sorts them into problems, neutral and positive comments.
---

# Are 3-star AliExpress reviews really complaints?

When you check a product, the 3-star reviews are where you expect the problems. This script uses the [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) with `filter=3`, reads every page, and sorts each comment into problem, neutral or positive.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

`GET /product/reviews?productId=...&filter=3` returns only the 3-star reviews. The script reads pages until `pagination.totalPages`, then checks each comment against a small word list. The reviews come in many languages (German, Spanish, Korean, Russian, Ukrainian, Polish, Arabic, Japanese), so the list is a starter that you should extend for your own buyers. Full script: [`examples/aliexpress_three_star_reviews.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/aliexpress_three_star_reviews.py).

```python
pages = read_all("3256807637171608", stars=3)
```

```bash
python aliexpress_three_star_reviews.py 3256807637171608
```

## Real output (20 Nov 2026)

```
filter=3 returned 33 reviews on 2 pages, but totalCount says 830
  problem     6  (18%)
  neutral    10  (30%)
  positive   17  (52%)

Reviews that mention a problem:
  CA  iPhone 16 Pro                   Good but quality could be better
  US  iPhone 16Pro Max                super thin and melted
  ES  iPhone 16Pro Max                чехол пришел помятым но в целом качество нормальное
  CL  iPhone 12 Mini                  Un poco pequeña pero bueno
  CA  iPhone 15                       pretty good, looks cheap tho
  CA  iPhone 16 Pro                   Could be better

Non-positive reviews for a Pro model: 11 of 16
Buyer countries in the 3-star group: DE 4, ES 4, KR 4, UA 4, PL 3
```

Only 6 of the 33 three-star reviews mention a problem (melted, looks cheap, small, dented in transit, "could be better"). Half of them are plainly positive, such as "Gut", "Good" or "Se ajusta bien", and another 10 are one-word answers like "Ok". Five of the 6 problem reviews are for 15 and 16 series phones.

## Things to know

- With `filter=3`, `pagination.totalCount` still says 830, the number for all reviews, while `totalPages` is 2. Use `totalPages` or the length of the list, not `totalCount`.
- The rating block lists 147 three-star ratings, but the filter returns only 33 reviews. Many buyers rate without writing a review, or the two counts are built differently.
- The word list is simple on purpose. It does not understand negation or sarcasm, so check the flagged reviews by eye.
- Some comments are in a different language from the buyer's country, for example a Russian comment from an ES buyer.

## Ideas

- Run the same check for 1-star and 2-star reviews, where real problems should be more common.
- Send the flagged comments to a translation API and read them in one language.
