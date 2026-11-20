---
title: See how much insider selling is under a 10b5-1 plan with Python
image: /assets/sec-insider-10b5-og.jpg
description: A Python script that reads Form 4 insider trades with the SEC Filings API on RapidAPI and shows which sales were made under a Rule 10b5-1 trading plan.
---

# How much insider selling is pre-planned?

A big insider sale looks scary, but many are made under a Rule 10b5-1 plan, set up in advance. The Form 4 footnote says so. The [SEC Filings API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sec-filings-api2) returns those footnotes, so you can split planned sales from the rest.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /v1/insiders/{ticker}/trades?limit=10&form=4`, keeps the open-market sales (`transactionCode` `S`), looks for `10b5-1` in the footnotes and totals the value per insider. Full script: [`examples/sec_insider_10b5.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/sec_insider_10b5.py).

```python
plan = any("10b5-1" in f for f in x.get("footnotes") or [])
```

```bash
python sec_insider_10b5.py AAPL 10
```

## Real output (20 Nov 2026)

```
10 Form 4 filings, 19 open-market sale lines

insider                sales   shares         USD  under plan
LEVINSON ARTHUR D          2   90,000  31,765,653        0/2
Newstead Jennifer          7   16,792   5,732,945        7/7
Parekh Kevan               5    1,392     480,315        5/5
Borders Ben                5    1,280     442,108        5/5

Total sold: $38,421,022; $6,655,368 (17%) was sold under a 10b5-1 plan
No plan footnote: 2026-11-18 LEVINSON ARTHUR D sold 36,792 at $352.26
No plan footnote: 2026-11-18 LEVINSON ARTHUR D sold 53,208 at $353.43
```

Most of the value comes from one director's two sales on 18 November, and those have no plan footnote. The three officers sold small amounts, all under a plan.

## Things to know

- A missing footnote does not prove there was no plan. It only means the filing text does not mention one.
- Each filing can hold several lines. The script counts only code `S` and skips tax withholding (`F`), option exercises (`M`) and gifts (`G`).
- `limit=10` returns the latest 10 filings. Raise it to look further back.

## Ideas

- Flag sales without a plan that are larger than a set value.
- Compare the sale prices with the stock price trend using another API.
