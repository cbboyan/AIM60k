# Changelog

Changes of this fork relative to the upstream AIM60k release (commit `33eb3c5`).

## Unreleased

- Normalized the TPTP problems with `scripts/normalize.py`:
  - named axioms, listed with their names in the new `problems/axioms.ax`
    (17 axioms common to all problems, 76 hypotheses);
  - axioms in a fixed order; the two variants of the `aim_lr` axiom written
    the same way;
  - conjecture named `goal_N_line_L` and written in a canonical form;
  - a one-line header naming the problem instead of the `ladr_to_tptp`
    symbol table (now in `axioms.ax`).
- The problems are logically unchanged; the LADR files are untouched.
