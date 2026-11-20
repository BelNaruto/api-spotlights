---
title: Rank every trim of a car by fuel economy and running cost with Python
image: /assets/carspecs-mpg-ladder-og.jpg
description: A Python script that lists every trim of a car model with city, highway and combined MPG, CO2 and yearly fuel cost, using the Car Specs API on RapidAPI.
---

# Rank every trim of a car by MPG and fuel cost with Python

Pick a make, model and year and see how its trims compare on fuel economy, CO2 and yearly fuel cost, so you can see which engine and gearbox combination is cheapest to run. It uses the [Car Specs API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/car-specs-api).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

The endpoint is `GET /mpg` with `make`, `model` and `year` (or a trim `id`). The response has `data.vehicle`, `data.range` (`combinedMin`, `combinedMax`) and `data.trims`. Each trim has `id`, `name`, `powertrain`, `drivetrain`, `transmission`, `engine`, `mpg` (`city`, `highway`, `combined`), `litersPer100Km`, `co2GramsPerMile`, `annualFuelCostUsd` and `mpgEstimateRevised`. Full script: [`examples/carspecs_mpg_ladder.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/carspecs_mpg_ladder.py).

```python
data = call("/mpg", make="honda", model="civic", year=2024)
for t in data["trims"]:
    print(t["id"], t["engine"], t["mpg"]["combined"], t["annualFuelCostUsd"])
```

```bash
python carspecs_mpg_ladder.py honda civic 2024
```

## Real output (20 Nov 2026)

The 2024 Honda Civic has **12 trims**, with combined economy from **24 to 36 MPG**. All of them are front-wheel drive. The best and worst of them:

| Id | Body | Engine | Gearbox | Combined MPG | CO2 g/mi | Fuel $/yr |
|----|------|--------|---------|--------------|----------|-----------|
| 47068 | 4Dr | 1.5 L turbo | Automatic (variable) | 36 | 243 | 1,650 |
| 47071 | 4Dr | 2 L | Automatic (variable) | 35 | 254 | 1,700 |
| 47097 | 5Dr | 1.5 L turbo | Automatic (variable) | 35 | 258 | 1,700 |
| 47069 | 4Dr | 1.5 L turbo | Automatic (AV-S7) | 34 | 260 | 1,750 |
| 47072 | 4Dr | 2 L | Automatic (AV-S7) | 33 | 266 | 1,800 |
| 47070 | 4Dr | 1.5 L turbo | Manual 6-speed | 31 | 285 | 2,400 |
| 47102 | 5Dr | 2 L | Manual 6-speed | 29 | 304 | 2,050 |
| 47582 | 5Dr | 2 L turbo | Manual 6-speed | 24 | 364 | 3,150 |

The cheapest trim to run costs 1,650 USD a year and the most expensive 3,150 USD, a difference of 1,500 USD.

## Things to know

- Two manual 1.5 L turbo trims have the same combined economy (31 MPG) but different yearly costs: 2,400 USD for the 4-door (id 47070) and 1,950 USD for the 5-door (id 47099). Check the cost field against the MPG before you show it to users.
- `year` defaults to 2024 in the playground, and the catalogue only lists makes that have specification data for that year.
- Costs are in USD and economy is in US MPG, so convert if you need litres per 100 km (it is in `litersPer100Km`).

## Ideas

- Loop over all models of a make with the `getModels` endpoint and find the cheapest trim to run.
- Feed the trim `id` into the compare endpoint (see the second tutorial).
