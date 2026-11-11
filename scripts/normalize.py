#!/usr/bin/env python3
"""Normalize the AIM60k TPTP problems.

For every problem X__goal_N:
- each axiom is matched (up to variable renaming, orientation of equations and
  order of literals) against problems/axioms.ax and written under its name, in
  the order of that file;
- the conjecture is written in a canonical form (fixed orientation, literal
  order and variable names) and named goal_N_line_L, where L is the proof line
  given by the comment in the LADR file;
- comments are dropped (symbols and names are documented in axioms.ax).

Two problems are then duplicates exactly when their files are identical apart
from the name of the conjecture. The LADR files are only read.

Usage: normalize.py [--problems DIR] [--out DIR] [--check]
  --out DIR   write the TPTP files to DIR instead of rewriting them in place
  --check     only report what would change
"""
import argparse
import itertools
import os
import re
import sys

VAR = re.compile(r"\b([A-Z][A-Za-z0-9_]*)\b")


def rename(s):
    m = {}
    return VAR.sub(lambda x: m.setdefault(x.group(1), "X%d" % len(m)), s)


def strip_parens(s):
    s = s.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        for i, ch in enumerate(s):
            depth += ch == "("
            depth -= ch == ")"
            if depth == 0 and i < len(s) - 1:
                return s
        s = s[1:-1].strip()
    return s


def split_top(s, sep):
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return parts


def literals(s):
    s = strip_parens(s)
    parts = split_top(s, "|")
    if len(parts) == 1:
        return [s]
    out = []
    for p in parts:
        out.extend(literals(p))
    return out


def literal(s):
    """Return (lhs, op, rhs) for an (in)equation literal."""
    s = strip_parens(s)
    neg = s.startswith("~")
    if neg:
        s = strip_parens(s[1:])
    m = re.match(r"^(.*?)\s*(!=|=)\s*(.*)$", s)
    if not m:
        raise ValueError("not an equation: %r" % s)
    a, op, b = m.groups()
    if neg:
        op = "=" if op == "!=" else "!="
    return a.strip(), op, b.strip()


def canon(clause):
    """Canonical text of a clause: the least renamed variant over all
    literal orders and equation orientations."""
    lits = [literal(x) for x in literals(clause)]
    best = None
    for perm in itertools.permutations(lits):
        for flips in itertools.product((0, 1), repeat=len(perm)):
            s = " | ".join(
                "%s %s %s" % ((b, op, a) if f else (a, op, b))
                for (a, op, b), f in zip(perm, flips)
            )
            s = rename(s)
            if best is None or s < best:
                best = s
    return best


def read_axioms(path):
    """name -> formula, canon -> name, and the order of names."""
    order, formula, by_canon = [], {}, {}
    for line in open(path):
        m = re.match(r"^cnf\((\w+),axiom,(.*)\)\.\s*$", line)
        if not m:
            continue
        name, f = m.groups()
        c = canon(f)
        if c in by_canon:
            sys.exit("axioms.ax: %s and %s are the same axiom" % (by_canon[c], name))
        order.append(name)
        formula[name] = f
        by_canon[c] = name
    return order, formula, by_canon


def parse_tptp(path):
    axioms, goal = [], None
    for line in open(path):
        m = re.match(r"^(cnf|fof)\((\w+),(\w+),(.*)\)\.\s*$", line)
        if not m:
            continue
        _, _, role, body = m.groups()
        if role == "conjecture":
            if goal is not None:
                raise ValueError("two conjectures")
            body = re.sub(r"^(\s*!\s*\[[^\]]*\]\s*:\s*)+", "", body)
            goal = body
        elif role == "axiom":
            axioms.append(body)
        else:
            raise ValueError("unexpected role %s" % role)
    if goal is None:
        raise ValueError("no conjecture")
    return axioms, goal


def ladr_line(path):
    for line in open(path):
        m = re.search(r"%\s*goal_(\d+)\s+line_(\d+)", line)
        if m:
            return int(m.group(1)), int(m.group(2))
    raise ValueError("no goal comment in %s" % path)


def goal_formula(c):
    vs = sorted(set(VAR.findall(c)), key=lambda v: int(v[1:]))
    body = c if " | " not in c else "(%s)" % c
    return "! [%s] : %s" % (",".join(vs), body) if vs else body


def normalize(name, tptp, ladr, order, formula, by_canon):
    axioms, goal = parse_tptp(tptp)
    names = set()
    for a in axioms:
        c = canon(a)
        if c not in by_canon:
            raise ValueError("unknown axiom: %s" % a)
        names.add(by_canon[c])
    if len(names) != len(axioms):
        raise ValueError("repeated axiom")
    n, line = ladr_line(ladr)
    if not name.endswith("__goal_%d" % n):
        raise ValueError("LADR comment says goal_%d" % n)
    out = ["cnf(%s,axiom,%s)." % (x, formula[x]) for x in order if x in names]
    out.append("fof(goal_%d_line_%d,conjecture,%s)." % (n, line, goal_formula(canon(goal))))
    return "\n".join(out) + "\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Normalize the AIM60k TPTP problems.")
    ap.add_argument("--problems", default=os.path.join(here, "..", "problems"))
    ap.add_argument("--out")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    order, formula, by_canon = read_axioms(os.path.join(a.problems, "axioms.ax"))
    tdir = os.path.join(a.problems, "tptp")
    out = a.out or tdir
    if not a.check:
        os.makedirs(out, exist_ok=True)
    errors, changed, total = [], 0, 0
    for f in sorted(os.listdir(tdir)):
        if not f.endswith(".p"):
            continue
        name = f[:-2]
        total += 1
        try:
            text = normalize(name, os.path.join(tdir, f),
                             os.path.join(a.problems, "ladr", name),
                             order, formula, by_canon)
        except (ValueError, OSError) as e:
            errors.append("%s: %s" % (name, e))
            continue
        target = os.path.join(out, f)
        old = open(target).read() if os.path.exists(target) else None
        if old != text:
            changed += 1
            if not a.check:
                with open(target, "w") as fh:
                    fh.write(text)
    for e in errors[:20]:
        print(e, file=sys.stderr)
    print("problems %d, changed %d, errors %d" % (total, changed, len(errors)))
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
