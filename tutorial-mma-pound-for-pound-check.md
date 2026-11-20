---
title: Check the UFC pound-for-pound list against the divisions with Python
image: /assets/mma-pound-for-pound-check-og.jpg
description: A Python script that compares the UFC men's pound-for-pound ranking with the division rankings from the MMA API on RapidAPI and finds fighters missing from the divisions.
---

# Is every pound-for-pound fighter in a division list?

The pound-for-pound list should name the best fighters across all divisions, so each one should also be ranked in a weight class. This script checks that with the [MMA API](https://rapidapi.com/belchiorarkad-FqvHs2EDOtP/api/mma-api1).

**What you need:** Python 3.8+, `pip install requests`, and a free RapidAPI key (`export RAPIDAPI_KEY=your_key`).

## The script

It calls `GET /rankings-ufc` once, builds a map from fighter name to division and rank, and looks up the 15 men's pound-for-pound fighters. It reuses `call` and `split` from the first script. Full script: [`examples/mma_pound_for_pound_check.py`](https://github.com/BelNaruto/api-spotlights/blob/main/examples/mma_pound_for_pound_check.py).

```python
where.setdefault(r["name"], (d["name"], r["rank"]))
```

```bash
python mma_pound_for_pound_check.py
```

## Real output (20 Nov 2026)

```
Men's Pound-for-Pound Top Rank

   1. Islam Makhachev         not in a division list
   2. Alexander Volkanovski   not in a division list
   3. Petr Yan                not in a division list
   4. Justin Gaethje          not in a division list
   5. Ilia Topuria            Ligero #1
   6. Joshua Van              not in a division list
   7. Sean Strickland         not in a division list
   8. Ciryl Gane              not in a division list
   9. Tom Aspinall            De peso pesado #1
  10. Merab Dvalishvili       Peso gallo #1
  11. Alex Pereira            Peso semipesado #3
  12. Khamzat Chimaev         Peso medio #1
  13. Arman Tsarukyan         Ligero #2
  14. Alexandre Pantoja       Peso mosca #1
  15. Carlos Ulberg           not in a division list

8 of 15 pound-for-pound fighters are not in any division list
```

Eight of the fifteen are not in any numbered division list on the day of the call. The API does not say why. It may be that champions or fighters who changed weight class are left out of the division lists, so check the source before you rely on it.

## Things to know

- The check uses only the numbered lists. The unnumbered repeated lists are ignored.
- A fighter can be missing because of a champion listing or a weight-class change. The response has no field that tells which.
- Name spelling must match exactly between the lists. All 7 matches here did.

## Ideas

- Add the women's pound-for-pound list and the same check.
- Compare with the `Champions ESPN` endpoint to see if the missing fighters are champions.
