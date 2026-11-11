#!/usr/bin/env python3
"""Swap problems between parts so that no part leaks into a later one.

Parts are ordered train < devel < holdout. A problem A leaks into a problem B
of a later part when A's axioms are a subset of B's and A's goal is B's goal
or more general (A's goal clause subsumes B's). Then any proof of A is a proof
of B. Such a pair is swapped: A goes to B's part and B to A's part, so the
later part keeps the problem with fewer assumptions or the more general goal,
and the earlier part the one with more assumptions or the special goal.

Swaps are done in rounds until no leak is left (each swap moves a smaller
axiom set or a more general goal to a later part, so this ends). Part sizes
do not change. Every swap is appended to problems/00SWAPS as
"round problem from to partner".

Run after normalize.py and dedup.py.

Usage: swap.py [--root DIR] [--dry-run]
"""
import argparse
import collections
import os
import re
import sys

PARTS = ["train", "devel", "holdout"]
RANK = {p: i for i, p in enumerate(PARTS)}


# --- goals as clauses of terms -------------------------------------------------

def tokens(s):
    return re.findall(r"!=|[A-Za-z_][A-Za-z0-9_]*|[(),=|]", s)


def parse_goal(body):
    """fof body '! [X0,..] : lit | lit' (literals s = t, s != t) -> clause."""
    body = re.sub(r"^\s*!\s*\[[^\]]*\]\s*:\s*", "", body.strip())
    t, i = tokens(body), 0

    def term():
        nonlocal i
        f = t[i]
        i += 1
        if i < len(t) and t[i] == "(":
            i += 1
            args = [term()]
            while t[i] == ",":
                i += 1
                args.append(term())
            i += 1  # ')'
            return (f, tuple(args))
        return f

    lits = []
    if t and t[0] == "(" and t[-1] == ")":
        t = t[1:-1]
    while i < len(t):
        a = term()
        op = t[i]
        i += 1
        b = term()
        lits.append((op, a, b))
        if i < len(t):
            i += 1  # '|'
    return tuple(lits)


def is_var(x):
    return isinstance(x, str) and x[0].isupper()


def match(g, s, th):
    """Extend substitution th so that g th == s; return it or None."""
    if is_var(g):
        if g in th:
            return th if th[g] == s else None
        th = dict(th)
        th[g] = s
        return th
    if isinstance(g, str) or isinstance(s, str):
        return th if g == s else None
    if g[0] != s[0] or len(g[1]) != len(s[1]):
        return None
    for x, y in zip(g[1], s[1]):
        th = match(x, y, th)
        if th is None:
            return None
    return th


def subsumes(gen, spec):
    """Some substitution maps every literal of gen onto a literal of spec."""
    def go(k, th):
        if k == len(gen):
            return True
        op, a, b = gen[k]
        for op2, c, d in spec:
            if op2 != op:
                continue
            for x, y in ((c, d), (d, c)):
                t1 = match(a, x, th)
                if t1 is not None:
                    t2 = match(b, y, t1)
                    if t2 is not None and go(k + 1, t2):
                        return True
        return False
    return go(0, {})


def head(x):
    return "*" if is_var(x) else (x[0] if isinstance(x, tuple) else x)


def lit_key(op, a, b):
    return (op,) + tuple(sorted((head(a), head(b))))


def index_key(clause):
    """Key of the most specific literal; a subsuming clause maps this literal
    onto some literal of the subsumed clause."""
    return min((lit_key(*l) for l in clause), key=lambda k: (k.count("*"), k))


def general_keys(clause):
    """All keys that a literal mapping onto some literal of clause can have."""
    out = set()
    for op, a, b in clause:
        for x in (head(a), "*"):
            for y in (head(b), "*"):
                out.add((op,) + tuple(sorted((x, y))))
    return out


# --- the split -------------------------------------------------------------------

def read_list(path):
    return [l.strip() for l in open(path) if l.strip()]


def load(prob):
    part, ax, goal, text = {}, {}, {}, {}
    for p in PARTS:
        for n in read_list(os.path.join(prob, p + ".names")):
            part[n] = p
    for n in part:
        names, g = [], None
        for line in open(os.path.join(prob, "tptp", n + ".p")):
            if line.startswith("cnf("):
                names.append(line[4:line.index(",")])
            elif line.startswith("fof("):
                g = line.split(",", 2)[2].rstrip().rstrip(".").rstrip()[:-1]
        ax[n] = frozenset(names)
        text[n] = g
        goal[n] = parse_goal(g)
    return part, ax, goal, text


def leak_pairs(part, ax, cand):
    """(a, b): a in an earlier part than b, a's axioms subset of b's, a's goal
    equal to or more general than b's."""
    out = []
    for b in sorted(part):
        if part[b] == PARTS[0]:
            continue
        for a in cand[b]:
            if RANK[part[a]] < RANK[part[b]] and ax[a] <= ax[b]:
                out.append((a, b))
    return out


def candidates(part, ax, goal, text):
    """For every problem b, the problems a whose goal equals or subsumes b's
    goal and whose axioms are a subset of b's (independent of the parts)."""
    index = collections.defaultdict(list)
    for n in part:
        index[index_key(goal[n])].append(n)
    cand = {}
    for b in part:
        found = set()
        for k in general_keys(goal[b]):
            for a in index.get(k, ()):
                if a == b or a in found or not ax[a] <= ax[b]:
                    continue
                if text[a] == text[b] or (len(goal[a]) <= len(goal[b]) and subsumes(goal[a], goal[b])):
                    found.add(a)
        cand[b] = sorted(found)
    return cand


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Swap leaking problems between parts.")
    ap.add_argument("--root", default=os.path.join(here, ".."))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    prob = os.path.join(a.root, "problems")

    part0, ax, goal, text = load(prob)
    cand = candidates(part0, ax, goal, text)
    part = dict(part0)
    log, rnd = [], 0
    while True:
        pairs = leak_pairs(part, ax, cand)
        kinds = collections.Counter("%s>%s" % (part[x], part[y]) for x, y in pairs)
        print("round %d: %d leaking pairs %s" % (rnd, len(pairs), dict(sorted(kinds.items()))))
        if not pairs:
            break
        rnd += 1
        used = set()
        for x, y in sorted(pairs, key=lambda p: (len(ax[p[0]]), p)):
            if x in used or y in used:
                continue
            px, py = part[x], part[y]
            part[x], part[y] = py, px
            log.append("%d %s %s %s %s" % (rnd, x, px, py, y))
            log.append("%d %s %s %s %s" % (rnd, y, py, px, x))
            used |= {x, y}
        if rnd > 100:
            sys.exit("no fixpoint after 100 rounds")

    changed = [n for n in part if part[n] != part0[n]]
    print("problems changing part: %d" % len(changed))
    for p in PARTS:
        print("  %-7s %6d" % (p, sum(1 for n in part if part[n] == p)))
    if a.dry_run or not log:
        return
    for p in PARTS:
        path = os.path.join(prob, p + ".names")
        old = read_list(path)
        keep = [n for n in old if part[n] == p]
        new = sorted(n for n in part if part[n] == p and part0[n] != p)
        with open(path, "w") as fh:
            fh.writelines(n + "\n" for n in keep + new)
    with open(os.path.join(prob, "00SWAPS"), "a") as fh:
        fh.writelines(l + "\n" for l in log)
    print("wrote %d swaps to problems/00SWAPS" % (len(log) // 2))


if __name__ == "__main__":
    main()
