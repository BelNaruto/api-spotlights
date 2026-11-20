---
title: Audit the UFC rankings from the MMA API with Python
image: /assets/mma-ufc-rankings-audit-og.jpg
description: A Python script that reads the UFC rankings with the MMA API on RapidAPI, lists the top fighters in every division and checks the lists for gaps and duplicates.
---

# Audit the UFC rankings

The [MMA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/mma-api1) returns the UFC rankings with `GET /rankings-ufc`. Before you build an app on a list like this, it is worth checking its shape. This script prints the top 2 of every list and compares the repeated lists.

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It reads the `rankings` array. Each item has a division `name` and a list of 15 `ranks` with `rank` and `name`. The script separates the lists that have rank numbers from those where `rank` is empty. Full script: [`examples/mma_ufc_rankings_audit.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/mma_ufc_rankings_audit.py).

```python
numbered = [d for d in rankings if d["ranks"] and d["ranks"][0]["rank"]]
plain = [d for d in rankings if d["ranks"] and not d["ranks"][0]["rank"]]
```

```bash
python mma_ufc_rankings_audit.py
```

## Real output (20 Nov 2026)

```
24 lists: 13 numbered, 11 without rank numbers

Numbered lists (top 2)
  Men's Pound-for-Pound Top Rank   1. Islam Makhachev       2. Alexander Volkanovski
  Peso mosca                       1. Alexandre Pantoja     2. Manel Kape
  Peso gallo                       1. Merab Dvalishvili     2. Sean O'Malley
  Peso pluma                       1. Movsar Evloev         2. Diego Lopes
  Ligero                           1. Ilia Topuria          2. Arman Tsarukyan
  Peso welter                      1. Ian Machado Garry     2. Carlos Prates
  Peso medio                       1. Khamzat Chimaev       2. Dricus Du Plessis
  Peso semipesado                  1. Magomed Ankalaev      2. Jiří Procházka
  De peso pesado                   1. Tom Aspinall          2. Alexander Volkov
  Women's Pound-for-Pound Top Rank 1. Kayla Harrison        2. Valentina Shevchenko
  Peso de la mujer                 1. Zhang Weili           2. Tatiana Suarez
  Women's Flyweight                1. Valentina Shevchenko  2. Alexa Grasso
  Gallo de las mujeres             1. Amanda Nunes          2. Joselyne Edwards

Unnumbered list leader vs numbered #1 (same division name)
  Peso mosca             Manel Kape            differs (numbered #1: Alexandre Pantoja)
  Peso gallo             Merab Dvalishvili     same
  Peso pluma             Movsar Evloev         same
  Ligero                 Ilia Topuria          same
  Peso welter            Carlos Prates         differs (numbered #1: Ian Machado Garry)
  Peso medio             Khamzat Chimaev       same
  Peso semipesado        Alex Pereira          differs (numbered #1: Magomed Ankalaev)
  De peso pesado         Tom Aspinall          same
  Peso de la mujer       Tatiana Suarez        differs (numbered #1: Zhang Weili)
  Women's Flyweight      Valentina Shevchenko  same
  Gallo de las mujeres   Joselyne Edwards      differs (numbered #1: Amanda Nunes)
```

The response has 24 lists. 13 are numbered. The other 11 repeat a division name with the `rank` field empty, and for 5 of them the first fighter is not the numbered #1.

## Things to know

- Division names are mixed: `Peso mosca`, `Peso welter` and `De peso pesado` are in Spanish, while `Women's Flyweight` is in English. Map them to your own names.
- The 11 lists without rank numbers repeat the division names. Decide which list you trust before you show a ranking.
- The response is a plain object with `rankings`, without a `success` flag.

## Ideas

- Run it every week and save the top 5 of each division to see changes.
- Map the Spanish division names to English with a small dictionary.
