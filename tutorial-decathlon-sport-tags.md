---
title: Check sport tags and data quality in a Decathlon collection with Python
image: /assets/decathlon-sport-tags-og.jpg
description: A Python script that reads a Decathlon collection with the Decathlon API on RapidAPI, groups products by sport tag and flags missing or odd tags.
---

# Check the sport tags of Decathlon products

Decathlon sorts products by sport, and the [Decathlon API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/decathlon-api) returns that in the `tags` of each product (`SPORT: road running`). If you want to filter a catalogue by sport, you need to know how reliable those tags are. This script checks them.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /collection/products` for the `new-arrivals` collection, reads the `SPORT:` tag of each product and prints the sports by number of products, the products with no sport tag, and the bags whose sport does not fit. Full script: [`examples/decathlon_sport_tags.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/decathlon_sport_tags.py).

```python
sport = next((t[7:] for t in product["tags"] if t.startswith("SPORT: ")), None)
```

```bash
python decathlon_sport_tags.py new-arrivals
```

## Real output (20 Nov 2026)

Product titles are shortened here to keep the lines short.

```
30 products, 10 distinct sport values
   7  road running
   6  mountain trekking
   6  (no sport tag)
   3  nature hiking
   2  5-a-side touch rugby
   2  city speed bikes

Without a SPORT tag: 6
  Gloves     Forclaz Adult MT500 Touchscree
  Backpack   Forclaz Travel 500 Organizer 4
  Water bag  Kiprun 15L Ultra Trail Running
  Water bag  Kiprun 5 L Trail Running Bag -
  Backpack   Quechua MH500 22L Lightweight 
  Backpack   Quechua MH500 25 L Hiking Back

Bags tagged with an unrelated sport: 5
  10L Laptop Backpack  ->  5-a-side Touch Rugby
  Roll-top backpack with laptop pock  ->  City speed bikes
  28L Sports Bag with Waterproof  ->  aerial yoga
  10L Laptop Backpack  ->  5-a-side Touch Rugby
  Roll-top backpack with laptop   ->  City speed bikes
```

Road running and mountain trekking cover most of the collection. Six products have no sport tag, and five bags have a tag that does not match them, for example a laptop backpack tagged `5-a-side Touch Rugby`.

## Things to know

- The same sport appears with different capital letters (`Road running` and `road running`), so compare tags in lower case.
- A sport tag is not always a good filter. Use `product_type` and the title as well.
- The `new-arrivals` collection holds repeated products: only 24 of the 30 titles were different, and the Simond down jacket appears several times.
- The list of bag sports in the script is a small example. Extend it for your own catalogue.

## Ideas

- Build a sport filter that falls back to `product_type` when the tag is missing.
- Run the same check on other collections and compare how many tags are missing.
