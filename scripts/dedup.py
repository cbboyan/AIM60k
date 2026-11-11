#!/usr/bin/env python3
"""Remove duplicate AIM60k problems.

Run after normalize.py. Two problems are duplicates when their TPTP files are
identical apart from the name of the conjecture. Of each group of duplicates
one problem is kept:
- the one in holdout, else in devel, else in train;
- within a part, the smallest original name, then the lowest goal number.

The other copies are moved to dups/, which mirrors the repository root:
- dups/problems/tptp/ and dups/problems/ladr/: their files;
- dups/problems/{train,devel,holdout}.names, 00ALL, 00E26_1s, 00P9_1s: their
  lines, taken out of the corresponding files in problems/;
- dups/problems/00DUPS: "removed kept" for every removed problem.

Usage: dedup.py [--root DIR] [--dry-run]
"""
import argparse
import collections
import hashlib
import os
import re
import sys

PARTS = ["holdout", "devel", "train"]  # keep priority
LISTS = ["train.names", "devel.names", "holdout.names", "00ALL", "00E26_1s", "00P9_1s"]


def content_key(path):
    text = open(path).read()
    text = re.sub(r"^fof\(goal_\d+_line_\d+,", "fof(goal,", text, flags=re.M)
    return hashlib.sha1(text.encode()).hexdigest()


def sort_key(part, name):
    orig, n = name.rsplit("__goal_", 1)
    return (PARTS.index(part), orig, int(n))


def read_list(path):
    return [l.strip() for l in open(path) if l.strip()]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Remove duplicate AIM60k problems.")
    ap.add_argument("--root", default=os.path.join(here, ".."))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    prob = os.path.join(a.root, "problems")
    dups = os.path.join(a.root, "dups", "problems")

    part = {}
    for p in PARTS:
        for n in read_list(os.path.join(prob, p + ".names")):
            if n in part:
                sys.exit("%s is in %s and %s" % (n, part[n], p))
            part[n] = p
    names = sorted(f[:-2] for f in os.listdir(os.path.join(prob, "tptp")) if f.endswith(".p"))
    if set(names) != set(part):
        sys.exit("tptp/ and the .names files disagree")

    groups = collections.defaultdict(list)
    for n in names:
        groups[content_key(os.path.join(prob, "tptp", n + ".p"))].append(n)
    kept_for = {}
    for g in groups.values():
        g.sort(key=lambda n: sort_key(part[n], n))
        for n in g[1:]:
            kept_for[n] = g[0]

    removed = collections.Counter(part[n] for n in kept_for)
    print("problems %d, distinct %d, duplicate groups %d, to remove %d"
          % (len(names), len(groups), sum(len(g) > 1 for g in groups.values()), len(kept_for)))
    for p in PARTS:
        total = sum(1 for n in part if part[n] == p)
        print("  %-7s %6d -> %6d (remove %d)" % (p, total, total - removed[p], removed[p]))
    if a.dry_run or not kept_for:
        return

    if os.path.exists(dups) and any(os.scandir(dups)):
        sys.exit("%s is not empty: dedup was already run" % dups)
    for d in ("tptp", "ladr"):
        os.makedirs(os.path.join(dups, d), exist_ok=True)
    for n in kept_for:
        os.rename(os.path.join(prob, "tptp", n + ".p"), os.path.join(dups, "tptp", n + ".p"))
        os.rename(os.path.join(prob, "ladr", n), os.path.join(dups, "ladr", n))
    for f in LISTS:
        lines = read_list(os.path.join(prob, f))
        with open(os.path.join(prob, f), "w") as fh:
            fh.writelines(n + "\n" for n in lines if n not in kept_for)
        with open(os.path.join(dups, f), "w") as fh:
            fh.writelines(n + "\n" for n in lines if n in kept_for)
    with open(os.path.join(dups, "00DUPS"), "w") as fh:
        fh.writelines("%s %s\n" % (n, kept_for[n]) for n in sorted(kept_for))
    print("moved %d problems to %s" % (len(kept_for), os.path.relpath(dups, a.root)))


if __name__ == "__main__":
    main()
