---
title: Compare two cars side by side and pick the winner per row with Python
image: /assets/carspecs-compare-og.jpg
description: A Python script that compares two to four car trims in one call, shows each spec in a row and marks the best value, using the Car Specs API on RapidAPI.
---

# Compare cars side by side with Python

Give the script two to four trim ids and it prints a comparison table with the best value marked on each row. It uses the [Car Specs API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /compare` with `ids`, a comma-separated list of 2 to 4 trim ids. The response has `data.vehicles` (`id`, `name`, `summary`), `data.comparison` and `data.specs`. Each row in `comparison` has the `values` for every vehicle and, where it makes sense, a `bestId`. Get trim ids from the `getMpg`, `getTrims` or `search` endpoints. Full script: [`examples/carspecs_compare.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/carspecs_compare.py).

```python
data = call("/compare", ids="41189,47069")
for row, info in data["comparison"].items():
    print(row, info["values"], info.get("bestId"))
```

```bash
python carspecs_compare.py 41189,47069
```

## Real output (20 Nov 2026)

A 2019 Tesla Model 3 Long Range (id 41189) against a 2024 Honda Civic 4Dr (id 47069). The API answered in 247 ms.

| Spec | Model 3 Long Range | Civic 4Dr | Best |
|------|--------------------|-----------|------|
| Combined economy | 130 MPGe | 34 MPG | Model 3 |
| City | 136 | 31 | Model 3 |
| Highway | 123 | 38 | Model 3 |
| Annual fuel cost (USD) | 600 | 1,750 | Model 3 |
| CO2 (g/mile) | 0 | 260 | Model 3 |
| Electric range (miles) | 310 | none | Model 3 |
| Engine | none | 1.5 L, 4 cylinders | n/a |
| Powertrain | Electric | Gasoline | n/a |
| Drivetrain | Rear-wheel | Front-wheel | n/a |
| Transmission | Automatic (A1) | Automatic (AV-S7) | n/a |
| Class | Midsize Cars | Midsize Cars | n/a |
| Passenger volume (cu ft) | 97 | 99 | n/a |
| Luggage volume (cu ft) | 15 | 15 | n/a |

## Things to know

- `combinedMpg` compares the electric car's MPGe with the petrol car's MPG, so the "best" flag is a plain number comparison. The script prints a note when the powertrains differ.
- Rows without a clear winner, such as passenger volume, have no `bestId`.
- Missing values come back as `null` (no engine displacement for the electric car), so handle them before doing arithmetic.

## Ideas

- Compare the cheapest and the most expensive trim from the MPG ladder.
- Turn the table into an HTML card for a "which car should I buy" page.
