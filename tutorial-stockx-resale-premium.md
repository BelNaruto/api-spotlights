---
title: Rank the most popular StockX sneakers by resale premium with Python
image: /assets/stockx-resale-premium-og.jpg
description: A Python script that ranks the most popular sneakers from the Sneaker Database - StockX API by resale premium over retail and flags the biggest price gaps between marketplaces.
---

# Rank the most popular sneakers by resale premium with Python

The `/mostpopular` endpoint of the [Sneaker Database - StockX API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sneaker-database-stockx) lists trending sneakers with their retail price, StockX lowest ask, last sale and the lowest price on up to four marketplaces. This script ranks them by premium over retail and shows where each pair is cheapest.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /mostpopular` with an optional `limit` (the docs say a maximum of 20). It returns a JSON array. Prices come back as strings (`"retailPrice": "95"`), so the script converts them first, then calculates `lowestAsk / retailPrice - 1` and picks the cheapest marketplace from `lowestResellPrice`. Full script: [`examples/stockx_resale_premium.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/stockx_resale_premium.py).

```python
shoes = call("/mostpopular", limit="20")
rows = analyse(shoes)      # sorted by premium, with the cheapest marketplace
```

```bash
python stockx_resale_premium.py 20
```

## Real output (20 Nov 2026)

```text
18 sneakers returned, 18 with a retail price and a StockX ask

Sneaker                                          Retail   Ask  Prem.  Cheapest
Jordan 1 Retro Low OG SP Travis Scott Sail Tro      155   227   +46%  stockX $227
Jordan 4 Retro Black Cat (2025)                     220   269   +22%  stockX $269
Nike Mind 001 Slide Black Chrome                     95   112   +18%  goat $97
Jordan 4 Retro OG Bred (2026)                       230   239    +4%  goat $219
Jordan 11 Retro Green Screen Monstars               255   262    +3%  goat $199
Nike Air Force 1 Low Supreme Black                  118   118    +0%  flightClub $93
Jordan 8 Retro Chrome (2026)                        215   204    -5%  goat $171
Jordan 5 Retro Black University Blue (2026)         220   199   -10%  stockX $199
Jordan 9 Retro OG Space Jam (2026)                  215   193   -10%  goat $160
Jordan 5 Retro Halloween                            220   175   -20%  stockX $175
Jordan 4 Retro Toro Bravo (2026)                    220   153   -30%  goat $120
Jordan 11 Retro Space Jam Magic Ball (Women's)      235   158   -33%  goat $140
Jordan 3 Retro True Blue (2026)                     230   147   -36%  goat $118
Nike Air Force 1 Low '07 White                      115    69   -40%  stockX $69
Birkenstock Boston Soft Footbed Suede Taupe         155    91   -41%  stockX $91
Jordan 7 Retro Miro (2026)                          255   141   -45%  goat $117
Timberland 6" Premium Waterproof Boot Wheat         220   117   -47%  goat $112
Maison Mihara Yasuhiro Hank OG Sole Canvas Low      220   106   -52%  stockX $106

Above retail: 5   Below retail: 12   Average premium: -15%

Biggest gap between marketplaces (highest lowest-price / cheapest lowest-price):
  Jordan 4 Retro Black Cat (2025)                 x3.9  (stockX $269, goat $1000, flightClub $1052)
  Maison Mihara Yasuhiro Hank OG Sole Canvas Low  x2.4  (stockX $106, stadiumGoods $129, flightClub $218, goat $253)
  Nike Air Force 1 Low Supreme Black              x1.7  (flightClub $93, stockX $118, goat $161)
```

Only **5 of the 18** trending pairs sell above retail, and the average premium is **-15%**. The Travis Scott Jordan 1 Low is the one with real heat at +46%, while most of the 2026 Jordan retros can be bought below retail. GOAT is the cheapest marketplace for 10 of the 18 pairs.

## Things to know

- I asked for `limit=20` and got **18** sneakers back.
- The response is large: about 150 KB for 18 products, because every item carries a long `imageLinks` list.
- `lowestResellPrice` is missing the Stadium Goods price for 17 of 18 products and the Flight Club price for 3 (Birkenstock, Timberland and Air Force 1 Low '07).
- The Jordan 4 Black Cat shows $1,000 on GOAT and $1,052 on Flight Club against $269 on StockX. That is probably stale data, so the script's price-gap check is a useful sanity filter.
- Some `styleID` values contain several ids joined by `/`, so do not assume one clean id per product.

## Ideas

- Pass each `styleID` to `/productprice` to see the cheapest size on every marketplace.
- Run it every morning and message yourself when a pair drops below retail.
