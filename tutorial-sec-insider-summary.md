---
title: Summarize insider buying and selling for any US stock with Python
image: /assets/sec-insider-summary-og.jpg
description: A Python script that reads the 90-day insider buy/sell summary from SEC Form 4 filings with the SEC Filings API on RapidAPI and prints a table per ticker.
---

# 90-day insider buy/sell summary from SEC filings

Company insiders (officers, directors, 10% owners) must report each trade on SEC Form 4. The [SEC Filings API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/sec-filings-api2) adds those filings up for you, so you can compare tickers without parsing EDGAR yourself.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /v1/insiders/{ticker}/summary?days=90` once per ticker and prints one table row each, with a short verdict. Full script: [`examples/sec_insider_summary.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/sec_insider_summary.py).

```python
d = call(f"/v1/insiders/{ticker}/summary", days=90)
print(d["sharesBought"], d["sharesSold"], d["netShares"], d["estimatedUsdSold"])
```

```bash
python sec_insider_summary.py AAPL
```

## Real output (20 Nov 2026)

```
ticker  insiders filings    bought      sold       net   est. USD sold  verdict
AAPL           8      27   716,919   836,802  -119,883     254,240,853  net selling

AAPL: insiders bought 0.86 shares for every share sold (API buySellRatio 0.16), estimated USD bought: 0
```

In the last 90 days, 8 Apple insiders filed 27 Form 4 filings. They sold about 836,802 shares, worth an estimated $254 million.

## Things to know

- The API returns `buySellRatio` 0.16, while the script's own division of shares gives 0.86. They are not the same number, so check which one you want before you use it in a signal.
- `sharesBought` is 716,919 but `estimatedUsdBought` is 0, so those shares do not look like open-market purchases (stock awards or option exercises are the likely reason). Treat `sharesBought` with care.
- The summary shows what was filed in the window, not why. Read the filings (see the [10b5-1 tutorial](tutorial-sec-insider-10b5.html)) before you read anything into the numbers.

## Ideas

- Run it on a watchlist every Monday and alert when net selling changes sign.
- Use the `insiderClusterBuys` endpoint to find stocks where several insiders buy in the same window.
