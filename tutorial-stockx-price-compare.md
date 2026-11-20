---
title: Compare sneaker resale prices across StockX, GOAT, Flight Club and Stadium Goods with Python
image: /assets/stockx-price-compare-og.jpg
description: A Python script that normalises the four marketplace price formats returned by the Sneaker Database - StockX API on RapidAPI and finds the cheapest place to buy each size.
---

# Compare sneaker resale prices across four marketplaces with Python

One request to the [Sneaker Database - StockX API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sneaker-database-stockx) returns resale prices from StockX, GOAT, Flight Club and Stadium Goods for a style ID. This script turns the four formats into one table and shows which marketplace is cheapest for each size.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /productprice` with `styleId`. The product fields (`shoeName`, `retailPrice`, `lowestAsk`, `lastSale`, `releaseDate`) are at the top level, and `resellPrices` holds one block per marketplace. **Each block has a different shape**, so the script normalises them first:

- `stockX` is a dict: `{"4": 109, "5": 142}`.
- `stadiumGoods` is a list of `{"size": "3", "price": 99}`.
- `flightClub` is an object with `newSizes`, where every entry has `size.display` and `lowestPriceOption.price`.
- `goat` is a list with one entry per size **and condition** (`new_no_defects`, `new_with_defects`, `used`), so the script keeps only new pairs without defects.

Full script: [`examples/stockx_price_compare.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/stockx_price_compare.py).

```python
d = call("/productprice", styleId="HQ6448")
by_size = lowest_by_size(d["resellPrices"])   # {"stockX": {4.0: 109, ...}, "goat": {...}, ...}
```

```bash
python stockx_price_compare.py HQ6448
```

## Real output (20 Nov 2026)

```text
adidas Yeezy Slide Onyx (HQ6448), retail $60, released 2022-03-07
StockX lowest ask $109, last sale $208

Cheapest new pair per marketplace (computed from the size data):
  GOAT           $71    size 4   (13 sizes listed)
  Stadium Goods  $99    size 3   (14 sizes listed)
  StockX         $109   size 4   (13 sizes listed)
  Flight Club    $122   size 4   (13 sizes listed)

What the lowestResellPrice block says:
  StockX         $109
  GOAT           $86   <- size data says $71
  Flight Club    $140   <- size data says $122
  Stadium Goods  $99

Best marketplace per size:
  size    3  SX   --     SG   $99    FC   --     GOAT --     -> Stadium Goods
  size    4  SX   $109   SG   $157   FC   $122   GOAT $71    -> GOAT
  size    5  SX   $142   SG   $235   FC   $147   GOAT $95    -> GOAT
  size    6  SX   $160   SG   $157   FC   $203   GOAT $137   -> GOAT
  size    7  SX   $151   SG   $178   FC   $193   GOAT $132   -> GOAT
  size    8  SX   $141   SG   $99    FC   $173   GOAT $127   -> Stadium Goods
  size    9  SX   $149   SG   $101   FC   $181   GOAT $127   -> Stadium Goods
  size   10  SX   $170   SG   $139   FC   $196   GOAT $143   -> Stadium Goods
  size   11  SX   $212   SG   $130   FC   $215   GOAT $172   -> Stadium Goods
  size   12  SX   $190   SG   $142   FC   $242   GOAT $189   -> Stadium Goods
  size   13  SX   $204   SG   $157   FC   $256   GOAT $178   -> Stadium Goods
  size   14  SX   $277   SG   $99    FC   $251   GOAT $176   -> Stadium Goods
  size   15  SX   $315   SG   $99    FC   $207   GOAT $140   -> Stadium Goods
  size   16  SX   $287   SG   $99    FC   $217   GOAT $151   -> Stadium Goods

Sizes won: Stadium Goods 10, GOAT 4, StockX 0, Flight Club 0
```

For the adidas Yeezy Slide Onyx (retail $60), GOAT has the cheapest new pair at **$71** (size 4). Stadium Goods wins 10 of the 14 sizes, mostly at the large end, and StockX and Flight Club win none.

## Things to know

- The `lowestResellPrice` block does not always match the size data. For GOAT it says $86, but the cheapest new pair in the size list is $71. For Flight Club it says $140, but the size list starts at $122. StockX and Stadium Goods match. Compute the minimum from the size data if you need exact numbers.
- Stadium Goods shows exactly $99 for five different sizes (3, 8, 14, 15 and 16). That looks like a floor price rather than a real ask, so treat it with care.
- Flight Club can list several prices for one size (size 9 has four), so the script keeps the lowest.
- Only sizes 4 to 16 are listed by StockX, GOAT and Flight Club. Stadium Goods also lists size 3.

## Ideas

- Run it for a list of style IDs from `/mostpopular` and print the best marketplace for your size.
- Save the output every day and alert when a size drops below retail.
