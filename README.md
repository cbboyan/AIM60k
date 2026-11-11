# 🔁 AIM60k (fork)

> The public part of the AIM60k theorem-proving benchmark, cleaned up:
> named axioms, no duplicate problems, and no train problem whose proof
> already proves a devel or holdout problem.

This is a fork of [**JUrban/AIM60k**](https://github.com/JUrban/AIM60k) by
Robert Veroff and Josef Urban. AIM60k is made from Prover9 proofs of the
[AIM project](https://www.cs.unm.edu/~veroff/AIM_REDONE/) (Michael Kinyon and
Robert Veroff): each problem `X__goal_N` asks to prove one step of the proof of
an original problem `X` from that original's axioms. See the upstream README
for how the problems and the train/devel/holdout split were made.

The fixes here are interim, until the upstream split is revised. The problems
themselves are logically unchanged.

## 📊 At a glance

| part    | upstream | duplicates removed | now    |
|---------|---------:|-------------------:|-------:|
| train   | 41,378   | 9,912              | 31,466 |
| devel   | 4,526    | 226                | 4,300  |
| holdout | 5,880    | 136                | 5,744  |
| total   | 51,784   | 10,274             | 41,510 |

On top of that, 3,769 problems moved between parts to stop leaks (part sizes
unchanged).

## 🧹 What changed, how, and why

### 🏷️ Named axioms, canonical files

`scripts/normalize.py`

- **Why.** Upstream names every axiom `sos`, which `tptp4X` rejects as a
  duplicate name, and writes the same problem in different ways (axiom order,
  orientation of equations, variable names), so duplicates are hard to see.
- **How.** The whole benchmark uses only 93 distinct axioms. They are listed
  under their names in [`problems/axioms.ax`](problems/axioms.ax): 17 occur in
  every problem, the 76 others are hypotheses of particular originals, named
  after R. Veroff's labels (`middle_bol`, `ak1`, `nil3_23`, ...). Every problem
  lists its axioms in the order of that file, the conjecture is written in a
  canonical form and named `goal_N_line_L` (goal `N`, from line `L` of the
  Prover9 proof), and a first comment line names the axioms, by group where
  possible:

  ```
  % axioms: BASE NUCSQ ak1
  ```

  Names and groups are explained in [`axiom-names.md`](axiom-names.md). The
  LADR files are unchanged.

### ✂️ Duplicates removed

`scripts/dedup.py`

- **Why.** Different originals often share their axioms (the 129 public
  originals have only 68 distinct axiom sets), so the same problem occurs under
  several names, often in different parts: 20.5% of devel and 29.6% of holdout
  were identical to a train problem.
- **How.** After normalization, identical problems have identical files apart
  from the name of the conjecture. Of each group one problem is kept: the one
  in holdout, else devel, else train; within a part, the smallest original
  name, then the lowest goal number. The others are moved to
  [`dups/`](dups), which has the same layout as the root;
  `dups/problems/00DUPS` maps each removed problem to the one kept.

### 🔀 Swaps against leaks

`scripts/swap.py`

- **Why.** A problem can still share its goal with a problem of a later part.
  If the earlier one (train before devel before holdout) has a subset of the
  axioms, or a more general goal, its proof is already a proof of the later
  one. After deduplication this held for about a quarter of devel and holdout.
- **How.** Each such pair is swapped: the later part gets the variant with
  fewer assumptions (or the more general goal), the earlier part the one with
  more assumptions, which is usually easier. This repeats until no such pair
  is left (three rounds). Part sizes do not change; every swap is listed in
  `problems/00SWAPS`.
- **Caveats.** About 72% of devel and holdout still have their goal in train,
  always with more axioms: a train proof that does not use the extra axioms is
  a proof of the evaluation problem too. The holdout originals are no longer
  kept whole. The 1 s baseline solve rates of the parts did not change
  (E 31%, Prover9 32% in each).

## 📁 Files

| path | contents |
|---|---|
| `problems/tptp/X__goal_N.p` | the problems in TPTP, normalized |
| `problems/ladr/X__goal_N` | the same problems in LADR (Prover9), as upstream |
| `problems/axioms.ax` | all 93 axioms with their names, and the axiom groups |
| `problems/{train,devel,holdout}.names` | the problems of each part, one name per line |
| `problems/00ALL` | all problems: the three lists together |
| `problems/00E26_1s`, `problems/00P9_1s` | upstream's baseline: problems solved by E 2.6 / Prover9 in 1 s (not rerun) |
| `problems/00SWAPS` | the swaps: `round problem from to partner` |
| `dups/problems/` | the removed duplicates, in the same layout, and `00DUPS` |
| `axiom-names.md` | how the axioms are named, and the groups |
| `scripts/` | `normalize.py`, `dedup.py`, `swap.py` (Python 3, standard library) |

## 🛠️ Reproduce

```sh
python3 scripts/normalize.py   # rewrite problems/tptp in canonical form
python3 scripts/dedup.py       # move duplicates to dups/
python3 scripts/swap.py        # swap leaking problems between parts
```

Each script prints what it does, and `dedup.py` and `swap.py` accept
`--dry-run`. Run in this order on an upstream checkout; rerunning any of them
changes nothing. Changes are recorded in the [changelog](CHANGELOG.md).

## ⚠️ Disclaimer

As upstream says: the problem database was built with scripts, and there
could be some exceptional cases with errors.
