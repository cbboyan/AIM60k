# Axiom names and groups

All 93 distinct axioms of AIM60k are listed with their names in
`problems/axioms.ax`. Every problem lists its axioms in the order of that file.

## Names

- The 17 axioms of every problem have descriptive names: `left_id`,
  `right_id`, `ld_cancel`, `ld_mult`, `rd_cancel`, `rd_mult` (loop axioms),
  `def_a`, `def_k`, `def_l`, `def_r`, `def_t` (definitions of the associator,
  the commutator and the inner mappings), and `aim_tt`, `aim_tl`, `aim_tr`,
  `aim_lr`, `aim_ll`, `aim_rr` (the inner mappings commute).
- The other 76 axioms are hypotheses of particular originals. They are named
  after the labels in R. Veroff's Prover9 input files, lowercased and with
  punctuation replaced by `_`: `middle Bol` → `middle_bol`, `aK1` → `ak1`,
  `nil3 23, aK3-Nr` → `nil3_23`, `aa1{x3/x4}` → `aa1_x3x4`. Five hypotheses
  have no label there and are named by the same convention: `aa1_x1x4`,
  `aa1_x2x4`, `aa1_x2x5`, `aa1_x3x5`, `aa1_x4x5`.

## Groups

Groups are written in capitals, so they cannot be confused with axiom names.

| group | axioms | meaning |
|---|---|---|
| `BASE` | the 17 axioms above | loop axioms, definitions, AIM conditions; in every problem |
| `NUCSQ` | `nucsq_l nucsq_m nucsq_r` | squares are in the left, middle and right nucleus |
| `AK` | `ak1 ak2 ak3 ka` | the conditions aK1, aK2, aK3 and Ka |
| `IMORD2` | `imord2_l imord2_r imord2_t` | the inner mappings L, R, T have order 2 |
| `AA1XX` | `aa1_x1x2 ... aa1_x4x5` (all 10) | aa1 with any two of its variables identified |
| `AA2XX` | `aa2_x2x3 aa2_x3x4` | aa2 with two adjacent variables identified |
| `AA3XX` | `aa3_x3x4 aa3_x4x5` | aa3 with two adjacent variables identified |
| `NIL3K` | `nil3_1 nil3_2 nil3_3 nil3_4 nil3_5 nil3_9 nil3_10 nil3_11` | lemmas of the nilpotency-class-3 proofs about K: KK, Ka, aK1–aK3 central, KK in the nuclei |
| `AA_NL` | `nil3_24 nil3_25 nil3_26` | aa1, aa2, aa3 are in the left nucleus |
| `AA_NM` | `nil3_27 nil3_28 nil3_29` | aa1, aa2, aa3 are in the middle nucleus |
| `AA_NR` | `nil3_30 nil3_31 nil3_32` | aa1, aa2, aa3 are in the right nucleus |

Every axiom is in at most one group. The groups are defined in
`problems/axioms.ax` (`% group NAME: axioms`), which `scripts/normalize.py`
reads.

## The axioms comment

Each problem starts with one comment line naming its axioms, for example

```
% axioms: BASE NUCSQ ak1
```

`BASE` comes first, then the groups whose axioms are all present (in the order
of the table), then the remaining axioms in the order of `axioms.ax`. A group is named only when all
of its axioms are in the problem. The comment depends only on the axioms, so
two problems with the same axioms have the same comment.
