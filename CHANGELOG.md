# Changelog

Changes of this fork relative to the upstream AIM60k release (commit `33eb3c5`).

## Unreleased

- Normalized the TPTP problems with `scripts/normalize.py`:
  - named axioms, listed with their names in the new `problems/axioms.ax`
    (17 axioms common to all problems, 76 hypotheses);
  - axioms in a fixed order; the two variants of the `aim_lr` axiom written
    the same way;
  - conjecture named `goal_N_line_L` and written in a canonical form;
  - the `ladr_to_tptp` symbol table is dropped (the symbols are documented in
    `axioms.ax`); instead a first line `% axioms: ...` names the axioms, e.g.
    `% axioms: BASE NUCSQ ak1`.
- Axiom groups, written in capitals and defined in `problems/axioms.ax`:
  `BASE` (the 17 axioms of every problem), `NUCSQ`, `AK`, `IMORD2`, `AA1XX`,
  `AA2XX`, `AA3XX`, `NIL3K`, `AA_NL`, `AA_NM`, `AA_NR`. Every axiom is in at
  most one group; a group is named in the `% axioms:` line when all its axioms
  are present.
- New `axiom-names.md`: how the axioms are named, and what the groups mean.
- Removed duplicate problems with `scripts/dedup.py`: 41,510 of 51,784 are
  distinct. One copy of each is kept (holdout before devel before train); the
  10,274 others are moved to `dups/`, with `dups/problems/00DUPS` mapping each
  to the problem kept. Train 31,466, devel 4,300, holdout 5,744.
- The problems are logically unchanged; the LADR files are untouched.
- The TPTP files now pass `tptp4X` (upstream's repeated formula name `sos` is
  rejected as a duplicate name).
