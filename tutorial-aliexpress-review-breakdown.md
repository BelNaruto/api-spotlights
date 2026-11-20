---
title: Break down AliExpress product reviews by phone model, country and shipping with Python
image: /assets/aliexpress-review-breakdown-og.jpg
description: A Python script that reads product reviews from the AliExpress Data API on RapidAPI and counts them by phone model, buyer country and shipping method.
---

# Break down AliExpress reviews by model, country and shipping

A product page can have hundreds of reviews, and each one says which variant was bought, where the buyer lives and which shipping option was used. This script uses the [AliExpress Data API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/aliexpress-data) to read the reviews of one phone case and turn them into counts.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /product/reviews` with `productId`, `page`, `pageSize` and `filter` (`all` or a star value from 1 to 5). The response has `pagination`, a `rating` block with the average and a breakdown, and a `reviews` list. Each review has `rating`, `country`, `sku` (the variant), `logistics` (the shipping option), `date` and `comment`. The `sku` text is messy (`Material:For iPhone 15Pro Max `, `For iPhone 15 ProMax`, `For iPhone 15 Pro Ships From:CHINA`), so the script cleans it before counting. Full script: [`examples/aliexpress_review_breakdown.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/aliexpress_review_breakdown.py).

```python
pages = [call("/product/reviews", productId="3256807637171608", page=p, pageSize=20, filter="all") for p in (1, 2)]
```

```bash
python aliexpress_review_breakdown.py 3256807637171608 2
```

## Real output (20 Nov 2026)

```
40 reviews read (830 reviews in total, page size 20)
Sample average 4.95 stars, API rating block says 4.9 (98%)
Rating breakdown counts 4953 ratings, pagination counts 830 reviews

Phone models:
  15 Pro Max                     4  ####
  13 Pro                         4  ####
  13                             4  ####
  16 Pro                         4  ####
  15 Pro                         4  ####
  15                             3  ###
  16                             2  ##
  14                             2  ##

Buyer countries:
  KR                             9  #########
  FR                             5  #####
  DE                             5  #####
  ES                             4  ####
  MX                             3  ###
  PL                             3  ###

Shipping:
  Standard Shipping             16  ################
  Premium Shipping              16  ################
  Standard                       7  #######
  Cainiao Super Economy          1  #

Average comment length by shipping:
  Standard Shipping              203 chars  (16 reviews)
  Premium Shipping               106 chars  (16 reviews)
  Standard                       161 chars  (7 reviews)
  Cainiao Super Economy           67 chars  (1 reviews)

Korea: 9 reviews, 9 with Premium shipping
```

The case is bought for every iPhone from the X to the 16 series, with the 13, 15 and 16 Pro models on top. Korea is the biggest country in this sample, and all 9 Korean reviews used Premium shipping. Premium reviews are also shorter: 106 characters on average, against 203 for Standard Shipping.

## Things to know

- The same shipping option appears with two names (`AliExpress Selection Standard Shipping` and `Aliexpress Selection Standard`), so group them by a cleaned name and decide yourself if they are one option.
- `pageSize=10` was sent in the playground and the response said `pageSize: 20`. The script asks for 20 so both sides agree.
- The rating block counts 4,953 ratings while `pagination.totalCount` says 830 reviews, so they count different things.
- The sample has 40 reviews of 830, so treat the percentages as a first look and read more pages for a real study.
- Every review in the sample has 0 up votes and 0 down votes.

## Ideas

- Compare the model mix of two competing products.
- Read all 42 pages with a short sleep between calls and save them to a CSV.
