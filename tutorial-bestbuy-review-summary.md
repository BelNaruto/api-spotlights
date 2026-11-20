---
title: Summarise what Best Buy customers like and dislike about a product with Python
image: /assets/bestbuy-review-summary-og.jpg
description: A Python script that turns the Best Buy review summary for a SKU into a star distribution plus the most mentioned pros and cons, using the BestBuy USA API on RapidAPI.
---

# Summarise Best Buy reviews for any product with Python

Give the script a Best Buy SKU and it prints the star distribution, the recommend rate and the topics reviewers mention most. It uses the [BestBuy USA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/bestbuy-usa).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/review/summary` with `skuId`. The response has `data.sku`, `data.verifiedPurchaseCount`, `data.overallStats` (`averageOverallRating`, `totalReviewCount`, `recommendedPercent`, `topRated`) and `data.distributions` with `ratings`, `pros` and `cons`, each entry holding a `value`, `count` and `roundedPercent`. Get SKU ids from the search endpoint (`skuId`). Full script: [`examples/bestbuy_review_summary.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/bestbuy_review_summary.py).

```python
d = call("/product/review/summary", skuId="6501022")
for x in d["distributions"]["pros"]:
    print(x["value"], x["count"])
```

```bash
python bestbuy_review_summary.py 6501022
```

## Real output (20 Nov 2026)

SKU `6501022` has an average of **4.8 stars** from **2,817 reviews**, **95% recommend** it, and Best Buy marks it as top rated. There were 2,752 verified purchases.

| Stars | Reviews | Share |
|-------|---------|-------|
| 5 | 2,434 | 86% |
| 4 | 216 | 8% |
| 3 | 78 | 3% |
| 2 | 25 | 1% |
| 1 | 64 | 2% |

Most mentioned positives: **Sound Quality (1,409)**, Comfort (386), Battery Life (341), Color (220) and Fit (99). The only negatives with enough mentions were **Volume (9)** and **Bass (4)**.

## Things to know

- The star counts add up to 2,817, the same as `totalReviewCount`, so the distribution and the overall stats agree.
- `pros` and `cons` percentages are shares of the mentions in that list, not of all reviews. Volume is 69% of cons but only 9 reviews.
- The 2-star row comes after the 1-star row in the response (order is 5, 4, 3, 1, 2), so sort by `value` before printing.

## Ideas

- Compare the summaries of two competing products and print which one wins on battery life.
- Combine it with the deal finder to find the best-rated products among the discounted ones.
