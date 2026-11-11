# AIM60k

AIM60k is a benchmark of 61,800 problems for automated theorem provers. Robert
Veroff and Josef Urban made it from the Prover9 proofs of 150 hard problems of
the [AIM project](https://www.cs.unm.edu/~veroff/AIM_REDONE/) by Michael Kinyon
and Robert Veroff.

This repository contains the public part: 51,784 problems coming from 129 of
the original problems. The remaining 10,016 problems (the secret part) are not
published. We keep them to evaluate systems ourselves.

## The AIM project

The AIM project works on the AIM conjecture in loop theory using the
automated theorem prover Prover9. An AIM loop is a loop whose inner mapping
group is abelian. The main conjecture says that for an AIM loop Q, Q/N(Q) is
an abelian group and Q/Z(Q) is a group, where N(Q) is the nucleus and Z(Q) the
center of Q. For background, see the [AIM project page](https://www.cs.unm.edu/~veroff/AIM_REDONE/)
and M. Kinyon, R. Veroff, P. Vojtěchovský, [*Loops with abelian inner mapping
groups: an application of automated deduction*](https://arxiv.org/abs/1509.05468).

## How the problems were made

Each original problem `X` is a Prover9 run that found a proof. From each proof,
a number of proof steps were selected as challenge goals. Each goal, with its
own axioms, is one problem, named `X__goal_N`. The 150 originals give 61,800
problems.

The steps are selected by a *striping* pattern, so that they get sparser
towards the end of the proof. The base pattern is

```
[[5, 3], [4, 5], [3, 8], [3, 13], [2, 21], [2, 34], [1, 55]]
```

where `[i, j]` means: select `i` lines that are `j` lines apart. One run of the
pattern covers 263 proof lines and selects 20 of them. Several runs can be
combined. For example, 3 runs give

```
[15, 3] [12, 5] [9, 8] [9, 13] [6, 21] [6, 34] [3, 55]
```

that is, 15 lines 3 apart, then 12 lines 5 apart, and so on, ending with 3 lines
55 apart. Shorter proofs end before reaching the last of these stripes. The
late goals are deep in the proof and far from the previous goal, so they are
usually the hardest.

## Train, devel, holdout and secret

The problems are divided into four parts:

| part    | use                                                  | originals | problems |
|---------|------------------------------------------------------|----------:|---------:|
| train   | training your system                                 |       108 |   41,378 |
| devel   | tuning your system and comparing its versions        |        10 |    4,526 |
| holdout | reporting results; do not train or tune on these     |       11* |   5,880* |
| secret  | not published; we keep these to test systems         |       21* |  10,016* |

\* Plus single goals moved from devel and train originals in step 2 below.

This was done in two steps.

**1. Whole originals.** We sorted the 150 originals by difficulty, measured by
the largest line number of their selected goals (roughly the length of the
proof), cut the sorted list into 10 groups from the longest proofs to the
shortest, and picked originals at random from each group. So every part has
easy, medium and hard originals, but secret and holdout take more from the
hardest group:

| part    | originals | picked                                                |
|---------|----------:|-------------------------------------------------------|
| secret  |        21 | 3 from the hardest group, 2 from each other group     |
| holdout |        11 | 2 from the hardest group, 1 from each other group     |
| devel   |        10 | 1 from each group                                     |
| train   |       108 | the rest                                              |

Each part was picked from the originals left over by the previous one, sorted
and grouped again.

Every goal of a secret original is in secret, and every goal of a holdout
original is in holdout. The goals of the devel and train originals are in devel
and train, except the few moved out in step 2. The secret and holdout originals
are kept whole because the goals of one original are steps of the same proof,
often only a few lines apart, so they are very similar. If some of them were in
train and others in holdout, a system could do well on holdout just because it
has seen the neighbouring steps.

**2. Late goals.** In the 118 devel and train originals, some single goals were
moved to secret and holdout as well, the later and harder ones more often. The
further a goal is from the previous selected goal in the proof, the more likely
it was moved: a goal 55 lines after the previous one went to secret with
probability 10% and to holdout with probability 10%, a goal 34 lines after it
with 34/55 of that, and so on, down to 3/55 of that for goals 3 lines apart.
(The first goal of each proof has no previous goal and was never moved.) So the
hard late goals are rarer in train and devel, but not missing. Proofs that end
before the 55-line stripe also contribute, with their widest stripes.

Of the 10,016 secret problems, 8,860 come from the 21 secret originals and 1,156
were moved in step 2. Of the 5,880 holdout problems, 4,720 come from the 11
holdout originals and 1,160 were moved in step 2.

A holdout problem `X__goal_N` whose `X` also has problems in `train.names` or
`devel.names` was moved there in step 2. The other holdout problems come from
whole holdout originals.

The split was made with the script `selsecret.py`:

```
selsecret.py PartialGoals --seed 2026 --top-frac 0.2 --frac 0.1
```

## Files

All files are in `problems/`:

| path                                   | contents                                                   |
|----------------------------------------|------------------------------------------------------------|
| `tptp/X__goal_N`                       | the problems in TPTP format, one file per problem          |
| `ladr/X__goal_N`                       | the same problems in LADR (Prover9) format                 |
| `train.names`, `devel.names`, `holdout.names` | the problems in each part, one name per line        |
| `00ALL`                                | all 51,784 public problems: the three lists together       |
| `00E26_1s`                             | baseline results of E 2.6 with a 1 s time limit            |
| `00P9_1s`                              | baseline results of Prover9 with a 1 s time limit          |

## Disclaimer

This problem database was built with scripts. There could be some exceptional
cases with errors.
## Changes in this fork

This fork makes interim fixes while the upstream split is being revised. See
`CHANGELOG.md` for the full list.

**Normalized TPTP files** (`scripts/normalize.py`). The problems are the same
as upstream, written in a canonical form:

- Every axiom has a name, the same in every problem. All 93 distinct axioms are
  listed in `problems/axioms.ax`, and every problem lists its axioms in the
  order of that file. The 17 axioms of every problem (loop axioms, the
  definitions of `a`, `k`, `l`, `r`, `t`, and the abelian inner mapping
  conditions) come first, then the hypotheses of the original. The hypotheses
  are named after the labels in R. Veroff's Prover9 input files (`nil3_23`,
  `middle_bol`, `ak1`, ...), lowercased to make them TPTP names.
- The conjecture is named `goal_N_line_L`: goal `N` of the original, taken from
  line `L` of its Prover9 proof (the comment in the LADR file).
- Equations, literals and variables of the conjecture are put in a fixed order,
  so two problems are the same exactly when their files are identical apart
  from the name of the conjecture.
- The only comment is a first line naming the axioms, by group where all
  axioms of a group are present, e.g. `% axioms: BASE NUCSQ ak1`. Names and
  groups are explained in `axiom-names.md`.

The LADR files are unchanged.

**Duplicates removed** (`scripts/dedup.py`). Different originals often share
their axioms (the 129 public originals have only 68 distinct axiom sets), so
the same problem occurs under several names. Of each group of identical
problems (identical files apart from the name of the conjecture) one is kept:
the one in holdout, else devel, else train; within a part, the smallest
original name, then the lowest goal number. The others are moved to `dups/`,
which has the same layout as the root (`dups/problems/tptp/`, `ladr/`, the
`.names` and `00*` lists), and `dups/problems/00DUPS` maps each removed problem
to the one kept in its place.

| part    | upstream | removed | now    |
|---------|---------:|--------:|-------:|
| train   | 41,378   | 9,912   | 31,466 |
| devel   | 4,526    | 226     | 4,300  |
| holdout | 5,880    | 136     | 5,744  |
| total   | 51,784   | 10,274  | 41,510 |

No problem now occurs twice, within a part or across parts. About a quarter of
devel and holdout still has its goal in train with a subset of the axioms;
this is not yet fixed. The baseline lists `00E26_1s` and `00P9_1s` were only
filtered; the results were not rerun.
