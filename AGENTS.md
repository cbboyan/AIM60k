# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

AIM60k: an ATP benchmark (Urban & Veroff), public part of 51,784 problems from 129
Prover9 proofs ("originals") of the AIM loop-theory project. Data only: no build, no
tests. `README.md` explains construction and the split; read it first.

This repo is a working fork (`cbboyan/AIM60k`) of the upstream release (`JUrban/AIM60k`, public). The
upstream split is being redone by its authors; quick fixes here (deduplication, axiom
naming, re-assigning goal variants between parts) are interim.

## Layout and invariants

Everything is in `problems/`:

- `tptp/X__goal_N.p` and `ladr/X__goal_N`: the same problem in two formats.
  The TPTP files are normalized (`scripts/normalize.py`, see below); the LADR
  files are upstream's and are not rewritten.
- `axioms.ax`: all 93 distinct axioms with their names, in the canonical order.
- `train.names`, `devel.names`, `holdout.names`: disjoint, one name per line, no `.p`.
  `00ALL` is their union (41,510 after dedup; upstream 51,784).
- `00E26_1s`, `00P9_1s`: names solved by E 2.6 / Prover9 at 1 s (upstream's runs,
  on the files before normalization).

`dups/problems/` mirrors `problems/` for the 10,274 duplicates removed by
`scripts/dedup.py` (same file and list layout), plus `00DUPS`: `removed kept` per
line. `problems/` + `dups/problems/` together give back upstream's 51,784.

Any change that adds, removes or renames problems must keep all of these in sync: both
format directories, the three `.names` files, `00ALL`, and the two baseline lists.

Facts about the files:

- Problem `X__goal_N`: original `X`, goal `N` (numbered in proof-line order). The LADR
  goal line carries `% goal_N  line_L` (the proof line).
- Normalized TPTP: `cnf(<name>,axiom,...)` lines in `axioms.ax` order, then
  `fof(goal_N_line_L,conjecture,...)` in canonical form (least variant over equation
  orientations and literal orders, variables `X0, X1, ...` by occurrence). Two
  problems are identical iff their files match apart from the conjecture name. The
  only comment is the first line, `% axioms: ...` (groups in capitals, defined in
  `axioms.ax` as `% group NAME: ...`, disjoint; see `axiom-names.md`).
- All goals of one original share its axiom set. 17 axioms occur in every problem
  (`left_id` ... `aim_rr`); the 76 hypotheses are named after the labels in R.
  Veroff's Prover9 `.in` files (lowercased, `nil3 23, aK3-Nr` -> `nil3_23`,
  `aa1{x3/x4}` -> `aa1_x3x4`). 68 distinct axiom sets. About 17% of goals are
  non-unit clauses.
- `normalize.py` aborts on any axiom not in `axioms.ax`; a new axiom must be added
  there first. It is idempotent (a rerun changes 0 files).

## Known data issues

- Duplicates (removed): 41,510 of upstream's 51,784 problems are distinct, never
  within one original, always across originals sharing an axiom set (129 originals,
  68 axiom sets). `dedup.py` keeps holdout > devel > train, then the smallest
  (original, goal number); it hashes each file with the conjecture name blanked.
- Only ~16.7k distinct goals; ~6.7k goals occur with more than one axiom set. If one
  copy's axioms are a subset of another's, a proof of the smaller one proves the
  larger one too (a split leak if the smaller is in train and the larger outside).
- The split was made per original (`selsecret.py`, not in the repo). After dedup, about
  25% of devel and holdout still leak: the same goal is in train with a subset of the
  axioms (`subset`) or a more general one (`instance`).

## Tools

`ladr_to_tptp`, `prover9`, `eprover` are on `PATH`. Python scripts should use the
standard library only. The tree is ~400 MB / ~100k small files: process it with one
script pass, not per-file shell loops.
